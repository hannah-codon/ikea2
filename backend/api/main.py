import db.crud as crud
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models import IkeaEntry, MaterialsTable
import pandas as pd

chairs_df = pd.read_csv("/mnt/data/projects/hackathons/mega-trend/data/all_chairs.csv")

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


@app.get("/entry/{url}")
def get_entry(url: str) -> IkeaEntry:
    article_nr = url.rstrip('/').split('/')[-1].split('-')[-1]
    name = url.rstrip('/').split('/')[-1].split('-')[0]

    article_row = chairs_df[chairs_df['article_number'] == article_nr]

    if article_row.empty:
        raise HTTPException(status_code=404, detail="Item not found")

    image_url = article_row['image_url'].iloc[0]
    article_nr = article_row['article_number'].iloc[0]
    price = article_row['price'].iloc[0]
    explanation = article_row['description'].iloc[0]
    eco_score = article_row['score'].iloc[0]

    return IkeaEntry(
        pid=article_nr,
        image_url=image_url,
        name=name,
        price=price,
        explanation=explanation,
        eco_score=eco_score,
    )


@app.get("/entry/similar/{pid}")
def get_similar_entries(pid: str) -> list[IkeaEntry]:
    items = crud.find_similar_items(pid)
    if not items:
        return []
    res = []
    for item in items:
        res.append(
            IkeaEntry(
                pid=item.article_id,
                image_url="https://www.ikea.com/se/en/images/products/groensta-chair-with-armrests-in-outdoor-grey-turquoise__1243805_pe920954_s5.jpg?f=xl",
                name="Chair",
                price=100,
                explanation="This is a chair",
                eco_score=10,
            )
        )
    return res


@app.post("/entry/compare/")
def compare_entries(pids: list[str]) -> str:
    if len(pids) != 2:
        raise HTTPException(status_code=400, detail="Exactly two IDs are required")
    explanation = crud.compare_items(chairs_df.loc[chairs_df["id"].isin(pids)])
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
    print("DB ITEM", db_item)
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
