from random import randrange
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
products = []

class Product(BaseModel):
    id: Optional[int] = 0
    number: str
    name: Optional[str] = None
    description: Optional[str] = None
    revision: str
    track: str = "main"

def find_product(key, value):
    for p in products:
        if p[key] == value:
            return p
    return None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/products")
def get_products():
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products in the database."
        )
    return products

@app.get("/products/latest")
def get_latest_product():
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products in the database."
        )
    product = products[-1]
    return product

@app.get("/products/revision={value}")
def get_product_by_revision(value):
    product = find_product("revision", value)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with revision {value} was not found."
        )
    return product

@app.get("/products/id={value}")
def get_product_by_id(value: int):
    product = find_product("id", value)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {value} was not found."
        )
    return product

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(new_product: Product):
    new_product_dict = new_product.dict()
    if new_product_dict["id"] == 0:
        new_product_dict["id"] = randrange(1, 100)
    products.append(new_product_dict)
    return products

@app.delete("/products/revision={value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_revision(value):
    for i, p in enumerate(products):
        if p["revision"] == value:
            products.pop(i)
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with revision {value} was not found."
    )

@app.delete("/products/id={value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(value: int):
    for i, p in enumerate(products):
        if p["id"] == value:
            products.pop(i)
            return None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id {value} was not found."
    )

@app.put("/products/{revision}")
def update_product_by_revision(revision, change_product: Product):
    change_product = change_product.dict()
    if change_product["id"] == 0:
        change_product["id"] = randrange(1, 100)
    for i, p in enumerate(products):
        if p["revision"] == revision:
            products[i] = change_product
            return products[i]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with revision {revision} was not found."
    )
