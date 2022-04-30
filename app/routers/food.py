from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.permissions import ensure_is_admin
from app.crud import food as food_crud
from app.dependencies.session import get_db
from app.schemas.food import Food, FoodData, FoodByCategory

router = APIRouter(prefix="/food", tags=["Food Menu"])

# at the end of the file, admin_router will be included in router
admin_router = APIRouter(dependencies=[Depends(ensure_is_admin)])

"""
 API Endpoints for Food Menu CRUD Operations.
"""


# Get Food Categories
@router.get("/categories/", response_model=list[str], dependencies=[Depends(ensure_is_admin)])
def get_food_categories(db: Session = Depends(get_db)):
    return food_crud.get_category(db=db)


# Show all food of food menu
@router.get("/menu-list/", response_model=list[Food])
def get_food(db: Session = Depends(get_db)):
    return food_crud.get_food(db=db)


# Show food by selected category
@router.get("/menu-by-category/", response_model=FoodByCategory)
def get_food_by_category(category: list[str] = Query(None), db: Session = Depends(get_db)):
    result: dict = {}
    for each_category in category:
        db_category = food_crud.get_food_by_category(db=db, category=each_category)
        result[each_category] = db_category
    return result


# Add new food item
@admin_router.post("/menu/", response_model=Food, dependencies=[Depends(ensure_is_admin)])
def create_food(new_food: FoodData, db: Session = Depends(get_db)):
    return food_crud.create_food(db=db, new_food=new_food)


# Update food details
@admin_router.put("/menu/{food_id}/", response_model=Food, dependencies=[Depends(ensure_is_admin)])
def update_food(food_id: int, food: FoodData, db: Session = Depends(get_db)):
    return food_crud.update_food(db=db, food=food, food_id=food_id)


# Delete food
@admin_router.delete("/menu/{food_id}/", dependencies=[Depends(ensure_is_admin)])
def delete_food(food_id: int, db: Session = Depends(get_db)):
    return food_crud.delete_food(db=db, food_id=food_id)


router.include_router(admin_router)
