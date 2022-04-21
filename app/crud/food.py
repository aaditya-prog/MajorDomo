from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.food import Food
from app.schemas.food import FoodData

"""
  Food operations

"""


# Check food exist or not
# If not, raise exception
def get_existing_food(db: Session, food_id: int):
    food_exist = db.query(Food).filter(Food.food_id == food_id).first()
    if food_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested food item doesn't exist in the menu.",
        )

    return food_exist


# Check same food present or not
def ensure_food_does_not_exist(db: Session, food_name: str):
    food_same = (
        db.query(Food).filter(func.lower(Food.food_name) == food_name.lower()).first()
    )
    if food_same:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Food already present"
        )


# Get Categories
def get_category(db: Session):
    breakpoint()
    dbquery = db.query(Food.food_category).distinct()
    values = [category[0] for category in dbquery]
    return values


# Get all food
def get_food(db: Session):
    return db.query(Food).all()


# Get food by category
def get_food_by_category(db: Session, category: str):
    return db.query(Food).filter(Food.food_category == category).all()


# Add food
def create_food(db: Session, new_food: FoodData):
    ensure_food_does_not_exist(db=db, food_name=new_food.food_name)

    db_food = Food(**new_food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


# Update food
def update_food(db: Session, food: FoodData, food_id: int):
    db_food = get_existing_food(db=db, food_id=food_id)
    db_food.food_name = food.food_name
    db_food.food_price = food.food_price
    db_food.food_category = food.food_category

    db.commit()
    db.refresh(db_food)
    return db_food


# Delete food
def delete_food(db: Session, food_id: int):
    food_remove = get_existing_food(db=db, food_id=food_id)
    db.delete(food_remove)
    db.commit()
    return {"detail": "Food removed"}
