import json
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from db.db import Item, SessionLocal
from db.models import ItemRead

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
    try:
        db_item = session.query(Item).filter(Item.article_id == article_id).first()
        if db_item is None:
            return None
        return ItemRead.model_validate(db_item)
    finally:
        session.close()


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


def compare_items(items: pd.DataFrame) -> str:

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
    )
    system_prompt_content = """
    I will give you information in json format about two Ikea chairs and I want
    you to give me an concise explanation in exactly two sentences why the chair with 
    the better score is actually better based on the given information. Lower score is better! Max 150 characters.
    Call the chairs by their name. No markdown. No need to mention the score directly.
    The information I give you about the chairs are:
    - score
    - materials
    - material score
    - durability 
    - weight
    - weight score

    This should give clear transperency by reasoning why one chair got a better score.
    """
    system_prompt = {"role": "system", "content": system_prompt_content}
    chairs = items.to_dict(orient="records")
    chairs_json = json.dumps(
        {"chair_1": chairs[0], "chair_2": chairs[1]}, indent=2, ensure_ascii=False
    )

    user_message = {"role": "user", "content": chairs_json}
    messages = [system_prompt, user_message]

    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    explanation = response.choices[0].message.content

    return explanation
