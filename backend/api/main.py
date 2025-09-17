import db.crud as crud
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models import IkeaEntry, MaterialsTable

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
    return IkeaEntry(
        pid="20557875",
        image_url="https://www.ikea.com/se/en/images/products/groensta-chair-with-armrests-in-outdoor-grey-turquoise__1243805_pe920954_s5.jpg?f=xl",
        name="Chair",
        price=100,
        explanation="This is a chair",
        eco_score=10,
    )


@app.get("/entry/similar/{pid}")
def get_similar_entries(pid: str) -> list[IkeaEntry]:
    return [
        IkeaEntry(
            pid="123",
            image_url="ikea.se/chair",
            name="Chair",
            price=100,
            explanation="This is a chair",
            eco_score=10,
        ),
        IkeaEntry(
            pid="1234",
            image_url="ikea.se/chair2",
            name="Chair2",
            price=200,
            explanation="This is also a chair",
            eco_score=8,
        ),
    ]


@app.post("/entry/compare/")
def compare_entries(pids: tuple[str, str]) -> str:
    if len(pids) != 2:
        raise HTTPException(status_code=400, detail="Exactly two IDs are required")
    return "Based on two IDS, explain how these items are similar, and how they differ in the climate aspect"


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


@app.get("/db_item/{item_id}")
def read_item(item_id: int):
    db_item = crud.get_item(item_id)
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
