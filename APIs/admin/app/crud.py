import itertools
import uuid
from datetime import date
from logging import exception

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, join, outerjoin

from admin.app import models, schemas

"""
  Food operations

"""


# Check food exist or not
# If not, raise exception
def exist_food(db: Session, food_id: int):
    food_exist = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    if food_exist is None:
        raise HTTPException(
            status_code=404, detail="The requested food item doesn't exist in the menu."
        )


# Check same food present or not
def same_food(db: Session, food_name: str):
    food_same = db.query(models.Food).filter(
        func.lower(models.Food.food_name) == food_name.lower()
    )
    if food_same:
        raise HTTPException(status_code=404, detail="Food already present")


# Get all food
def get_food(db: Session):
    return db.query(models.Food).all()


# Get food by category
def get_food_by_category(db: Session, category: str):
    return db.query(models.Food).filter(models.Food.food_category == category).all()


# Add food
def create_food(db: Session, new_food: schemas.FoodData):
    same_food(db=db, food_name=new_food.food_name)

    db_food = models.Food(**new_food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


# Update food
def update_food(db: Session, food: schemas.FoodData, food_id: int):
    exist_food(db=db, food_id=food_id)
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db_food.food_name = food.food_name
    db_food.food_price = food.food_price
    db_food.food_category = food.food_category

    db.commit()
    db.refresh(db_food)
    return db_food


# Delete food
def delete_food(db: Session, food_id: int):
    exist_food(db=db, food_id=food_id)
    food_remove = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db.delete(food_remove)
    db.commit()
    return {"Food removed"}
