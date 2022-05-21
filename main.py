import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.routers import food, inventory, order, user


description = """
Based on the authentication levels, these API endpoints allow you to perform the following actions. ✔️

## Customer

You will be able to:

* **View menu, add order items.**
* ****


## Admin

You will be able to:

* **Register, Login, Profile, Change Password.**
* **Create, Read, Retrieve and Delete -  Staffs, Menu items.**
* **View Reports**
* ****


## Cashier

You will be able to:

* **Register, Login, Profile, Change Password.**
* **View, Complete Orders**
* ****


## Kitchen Staff

You will be able to:

* **Register Staffs, Login, Profile, Change Password.**
* **Confirm Orders.**
* ****


## Inventory Staff

You will be able to:

* **Login, Profile, Change Password.**
* **Create, Read, Retrieve and Delete -  Inventory Items**
* ****


"""
# An instance of FastAPI class.
app = FastAPI(
    title="Restaurant Management System (RMS) API",
    # description=description,
    # version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Aaditya Dulal",
        "url": "https://aadityadulal.com",
        "email": "artdityadulal@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


# Including the routers of the submodules respectively.
app.include_router(user.router)
app.include_router(inventory.router)
app.include_router(order.router)
app.include_router(food.router)


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='192.168.1.17')
