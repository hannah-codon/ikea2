from db.db import Item, SessionLocal
from db.models import ItemRead


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
