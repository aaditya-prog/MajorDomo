import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from admin import admin
from inventory import inventory

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

* **Register, Login, Profile, Change Password.**
* **Confirm Orders.**
* ****


## Inventory Staff

You will be able to:

* **Register, Login, Profile, Change Password.**
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

origins = ["http://localhost:3000", "localhost:3000", "http://localhost:8000", "localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including the routers of the submodules respectively.
app.include_router(admin.router)
app.include_router(inventory.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5005)
