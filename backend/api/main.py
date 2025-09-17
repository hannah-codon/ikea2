import db.crud as crud
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models import IkeaEntry, MaterialsTable

chairs_df = pd.read_csv(
    "/mnt/data/projects/hackathons/mega-trend/data/all_chairs_w_explanation_v3.csv"
)
chairs_df["article_number"] = chairs_df["article_number"].astype(str)

print("Chairs DF SIZE", chairs_df.shape)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return {"message": "Hello, World"}


def get_ikea_entry_from_csv(df: pd.DataFrame, article_nr: str) -> IkeaEntry | None:
    article_row = df[df["article_number"] == str(article_nr)]
    if article_row.empty:
        return None
    image_url = article_row["image_url"].iloc[0]
    article_nr = article_row["article_number"].iloc[0]
    price = article_row["price"].iloc[0]
    explanation = article_row["gen_description"].iloc[0]
    eco_score = article_row["rel_score"].iloc[0]
    name = article_row["name"].iloc[0]
    print("NAME", name)
    return IkeaEntry(
        pid=article_nr,
        image_url=image_url,
        name=name,
        price=price,
        explanation=explanation,
        eco_score=eco_score,
    )


@app.post("/entry/")
def get_entry(url: str) -> IkeaEntry:
    article_nr = url.rstrip("/").split("/")[-1].split("-")[-1]
    article_nr = article_nr.replace("s", "")
    # If article number starts with 0, remove it
    if article_nr.startswith("0"):
        article_nr = article_nr[1:]

    ikea_entry = get_ikea_entry_from_csv(chairs_df, article_nr)
    name = url.rstrip("/").split("/")[-1].split("-")[0]
    name = name.lower().capitalize()
    ikea_entry.name = name

    return ikea_entry


@app.get("/entry/similar/{pid}")
def get_similar_entries(pid: str) -> list[IkeaEntry]:
    items = crud.find_similar_items(pid)
    print(len(items))

    og_name = str(chairs_df[chairs_df['article_number'] == pid]['name'].iloc[0])
    og_score = chairs_df[chairs_df['article_number'] == pid]['rel_score'].iloc[0]
    if not items:
        return []
    res = []
    for item in items:
        article_id = item.article_id
        print("Found similar item:", article_id)
        ikea_entry = get_ikea_entry_from_csv(chairs_df, article_id)
        if ikea_entry is not None:
            if ikea_entry.name == og_name:
                continue
            elif ikea_entry.score > og_score:
                continue
            else:
                res.append(ikea_entry)
    return res


@app.post("/entry/compare/")
def compare_entries(pids: list[str]) -> str:
    print("find me pids", pids)
    if len(pids) != 2:
        raise HTTPException(status_code=400, detail="Exactly two IDs are required")
    explanation = crud.compare_items(
        chairs_df.loc[chairs_df["article_number"].isin(pids)]
    )
    return explanation


@app.get("/materials-table/")
def get_materials_table() -> MaterialsTable:
    return MaterialsTable(
        headers=["Material", "Ranking"],
        rows=[
            ["Wood", "1"],
            ["Steel", "2"],
            ["Plastic", "3"],
        ],
    )


@app.get("/db_item/{article_id}")
def read_item(article_id: str):
    db_item = crud.get_item(article_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.post("/db_item/")
def create_db_item(article_id: str):
    mock_embedding = [0.1] * 384  # Replace with actual embedding generation logic
    db_item = crud.write_item(article_id=article_id, embedding=mock_embedding)
    return db_item


@app.get("/similar_items/")
def get_similar_db_items(article_id: str, top_k: int = 5):
    items = crud.find_similar_items(article_id, top_k)
    return items


@app.delete("/db_items/")
def delete_all_db_items():
    num_deleted = crud.delete_all_items()
    return {"deleted": num_deleted}


@app.get("/db_items/")
def get_all_db_items():
    items = crud.get_all_items()
    return items
