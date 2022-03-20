import datetime
from typing import List, Optional

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal, engine

from .app import crud
from .app import models as models
from .app import schemas as schemas

models.Base.metadata.create_all(bind=engine)

# An instance of APIRouter.
router = APIRouter()


# Creating a dependency function to make connection with the database.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
 API Endpoints for "Inventory" submodule.

"""


# Show all items in the inventory.
@router.get("/item_list/", tags=["Inventory CRUD"])
def get_item(db: Session = Depends(get_db)):
    return crud.get_items(db=db)


# Show items by selected category
@router.get("/item_by_category/", tags=["Inventory CRUD"])
def get_item_category(category: List[str] = Query(None), db: Session = Depends(get_db)):
    result = []
    for each_category in category:
        db_category = crud.get_item_by_category(db=db, category=each_category)
        result = result + db_category
    return result


# Add new item in inventory.
@router.post("/add_item/", tags=["Inventory CRUD"])
def create_item(new_item: schemas.InventoryData, db: Session = Depends(get_db)):
    return crud.create_item(db=db, new_item=new_item)


# Update item details.
@router.put("/update_item/{item_id}/", tags=["Inventory CRUD"])
def update_item(
    item_id: int, item: schemas.InventoryData, db: Session = Depends(get_db)
):
    return crud.update_item(db=db, item=item, item_id=item_id)


# Delete item from inventory.
@router.delete("/delete_item/{item_id}/", tags=["Inventory CRUD"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db=db, item_id=item_id)
