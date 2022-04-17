from typing import Optional

from auth.permissions import ensure_is_inventory_staff
from config import database
from crud import inventory as inventory_crud
from fastapi import APIRouter, Depends, Query
from schemas.inventory import InventoryData, Item, ItemByCategory
from sqlalchemy.orm import Session

# An instance of APIRouter.
router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    dependencies=[Depends(ensure_is_inventory_staff)]
)


# Creating a dependency function to make connection with the database.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
 API Endpoints for "Inventory" submodule.

"""


# Show all items in the inventory.
@router.get("/item-list/", response_model=list[Item])
def get_item(
    offset: Optional[int] = 0,
    limit: Optional[int] = 20,
    db: Session = Depends(get_db)
):
    return inventory_crud.get_items(db=db, offset=offset, limit=limit)


# Show items by selected category
@router.get("/item-by-category/", response_model=ItemByCategory)
def get_item_category(
    category: list[str] = Query(...),
    db: Session = Depends(get_db)
):
    result: dict = {}
    for each_category in category:
        db_category = inventory_crud.get_item_by_category(
            db=db, category=each_category
        )
        result[each_category] = db_category
    return result


# Add new item in inventory.
@router.post("/item/", response_model=Item)
def create_item(new_item: InventoryData, db: Session = Depends(get_db)):
    return inventory_crud.create_item(db=db, new_item=new_item)


# Update item details.
@router.put("/item/{item_id}/", response_model=Item)
def update_item(
    item_id: int, item: InventoryData, db: Session = Depends(get_db)
):
    return inventory_crud.update_item(db=db, item=item, item_id=item_id)


# Delete item from inventory.
@router.delete("/item/{item_id}/")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return inventory_crud.delete_item(db=db, item_id=item_id)
