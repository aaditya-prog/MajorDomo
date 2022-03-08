import uvicorn
from fastapi import FastAPI

from admin import admin

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
# app = FastAPI(
#     title="Restaurant Management System (RMS) API",
#     description=description,
#     # version="0.0.1",
#     # terms_of_service="http://example.com/terms/",
#     contact={
#         "name": "Aaditya Dulal",
#         "url": "https://aadityadulal.com",
#         "email": "artdityadulal@gmail.com",
#     },
# )
app = FastAPI()
app.include_router(admin.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5005)
