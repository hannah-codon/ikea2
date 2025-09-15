from fastapi import FastAPI
from src.models import IkeaEntry, MaterialsTable
from fastapi import HTTPException
app = FastAPI()


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
def compare_entries(pids: list[str, str]) -> str:
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