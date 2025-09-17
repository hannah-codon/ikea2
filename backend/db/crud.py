from db.db import Item, SessionLocal


def create_item(name: str, embedding: list):
    session = SessionLocal()
    db_item = Item(name=name, embedding=embedding)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_item(item_id: int):
    session = SessionLocal()
    return session.query(Item).filter(Item.id == item_id).first()
