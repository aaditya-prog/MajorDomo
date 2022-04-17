from .food import Food
from .inventory import Inventory
from .order import Orders
from .user import User

# For autogenerate to work with alembic
# Base and the models have to be in the same module
# One way of achieving that is importing Base and all the models here
# Then the Base in this module is imported into the env.py file for alembic

__all__ = ["Food", "Inventory", "Orders", "User"]
