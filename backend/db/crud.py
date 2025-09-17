from db.db import Item, SessionLocal
from db.models import ItemRead
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def create_item(name: str, embedding: list):
    session = SessionLocal()
    db_item = Item(name=name, embedding=embedding)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    db_item = ItemRead.model_validate(db_item)
    return db_item


def get_item(article_id: str):
    session = SessionLocal()
    db_item = session.query(Item).filter(Item.article_id == article_id).first()
    return ItemRead.model_validate(db_item)


def write_item(article_id: str, embedding: list[float]):
    session = SessionLocal()
    db_item = Item(article_id=article_id, embedding=embedding)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    db_item = ItemRead.model_validate(db_item)
    return db_item


def find_similar_items(article_id: str, top_k: int = 5):
    session = SessionLocal()
    item = get_item(article_id)
    if item is None:
        return []
    embedding = item.embedding
    res = (
        session.query(Item)
        .order_by(Item.embedding.cosine_distance(embedding))
        .limit(top_k)
        .all()
    )
    return [ItemRead.model_validate(i) for i in res]


def delete_all_items():
    session = SessionLocal()
    num_deleted = session.query(Item).delete()
    session.commit()
    return num_deleted


def get_all_items():
    session = SessionLocal()
    items = session.query(Item).all()
    return [ItemRead.model_validate(i) for i in items]

def compare_items(pids_info: list[str])-> str:
    client = OpenAI(
            api_key= os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
            )
    system_prompt_content = """
    I will give you information about two Ikea chairs and I want
    you to give me an explanation in two sentences why the chair with 
    the better score is actually better based on the other information.
    The information I give you about the chairs are:
    - score
    - materials
    - material score
    - durability 
    - weight
    - weight score
    This should give some transperency why one chair got a better score.
    """
    system_prompt = {
        "role": "system",
        "content": system_prompt_content
    }
    user_message = {
        "role": "user",
        "content":pids_info
    }
    messages = [
        system_prompt,
        user_message
    ]

    response = client.chat.completions.create(
        model="gpt-5",  
        messages=messages
    )
    explanation= response.choices[0].message.content

    return explanation
