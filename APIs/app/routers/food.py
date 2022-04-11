from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crud import food as food_crud
from schemas.food import FoodData

import database

router = APIRouter(prefix="/food", tags=["Food Menu"])

"""
 API Endpoints for Food Menu CRUD Operations.
"""


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Show all food of food menu
@router.get("/menu-list/")
def get_food(db: Session = Depends(get_db)):
    return food_crud.get_food(db=db)


# Show food by selected category
@router.get("/menu-by-category/")
def get_food_category(
    category: List[str] = Query(None), db: Session = Depends(get_db)
):
    result: List = []
    for each_category in category:
        db_category = food_crud.get_food_by_category(
            db=db, category=each_category
        )
        result = result + db_category
    return result


# Add new food item
@router.post("/menu/")
def create_food(new_food: FoodData, db: Session = Depends(get_db)):
    return food_crud.create_food(db=db, new_food=new_food)


# Update food details
@router.put("/menu/{food_id}/")
def update_food(food_id: int, food: FoodData, db: Session = Depends(get_db)):
    return food_crud.update_food(db=db, food=food, food_id=food_id)


# Delete food
@router.delete("/menu/{food_id}/")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    return food_crud.delete_food(db=db, food_id=food_id)
