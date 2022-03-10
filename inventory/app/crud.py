from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from inventory.app import models, schemas

"""
  Inventory operations

"""


# Check if item exists in the inventory
# If not, raise exception
def exist_item(db: Session, item_id: int):
    item_exist = (
        db.query(models.Inventory).filter(models.Inventory.item_id == item_id).first()
    )
    if item_exist is None:
        raise HTTPException(status_code=404, detail="Item not found in inventory")


# Check if item is available in required quantity
# If not, raise exception
def item_available(db: Session, item_id: int, q: int):
    available_item = (
        db.query(models.Inventory)
        .filter(
            and_(
                models.Inventory.item_id == item_id, models.Inventory.item_quantity >= q
            )
        )
        .first()
    )
    if available_item is None:
        raise HTTPException(status_code=404, detail="Item out of stock")


# Get all items from the inventory.
def get_items(db: Session):
    return db.query(models.Inventory).all()


# Get item by category.
def get_item_by_category(db: Session, category: str):
    return (
        db.query(models.Inventory)
        .filter(models.Inventory.item_category == category)
        .all()
    )


# Add Item
def create_item(db: Session, new_item: schemas.InventoryData):
    db_item = models.Inventory(**new_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Update existing item
def update_item(db: Session, item: schemas.InventoryData, item_id: int):
    exist_item(db=db, item_id=item_id)
    item_in_inventory = (
        db.query(models.Inventory).filter(models.Inventory.item_id == item_id).first()
    )
    item_in_inventory.item_name = item.item_name
    item_in_inventory.item_price = item.item_price
    item_in_inventory.item_category = item.item_category
    item_in_inventory.item_quantity = item.item_quantity

    db.commit()
    db.refresh(item_in_inventory)
    return item_in_inventory


# Delete item by id
def delete_item(db: Session, item_id: int):
    exist_item(db=db, item_id=item_id)
    item_remove = (
        db.query(models.Inventory).filter(models.Inventory.item_id == item_id).first()
    )
    db.delete(item_remove)
    db.commit()
    return {"Item deleted from inventory"}
