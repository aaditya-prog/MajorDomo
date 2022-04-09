from datetime import date

from pydantic import BaseModel, validator


class OrderBase(BaseModel):
    items: list[int]
    table: int

    @validator('table')
    def table_is_valid(cls, v):
        if v < 1 or v > 8:
            raise ValueError('Not a valid table number')
        return v


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int
    order_date: date
