from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crud import food as food_crud
from schemas.food import Food, FoodData, FoodByCategory

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
@router.get("/menu-list/", response_model=list[Food])
def get_food(db: Session = Depends(get_db)):
    return food_crud.get_food(db=db)


# Show food by selected category
@router.get("/menu-by-category/", response_model=FoodByCategory)
def get_food_category(
    category: list[str] = Query(None), db: Session = Depends(get_db)
):
    result: dict = {}
    for each_category in category:
        db_category = food_crud.get_food_by_category(
            db=db, category=each_category
        )
        result[each_category] = db_category
    return result


# Add new food item
@router.post("/menu/", response_model=Food)
def create_food(new_food: FoodData, db: Session = Depends(get_db)):
    return food_crud.create_food(db=db, new_food=new_food)


# Update food details
@router.put("/menu/{food_id}/", response_model=Food)
def update_food(food_id: int, food: FoodData, db: Session = Depends(get_db)):
    return food_crud.update_food(db=db, food=food, food_id=food_id)


# Delete food
@router.delete("/menu/{food_id}/")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    return food_crud.delete_food(db=db, food_id=food_id)
