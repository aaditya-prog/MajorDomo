from pydantic import BaseModel


class FoodData(BaseModel):
    food_name: str
    food_category: str
    food_price: float


class Food(FoodData):
    food_id: int

    class Config:
        orm_mode = True


FoodByCategory = dict[str, list[Food]]
