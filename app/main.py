"""
This module provides a FastAPI-based web service for managing and querying product information.
"""

import sys
import time
from typing import Optional
from random import randrange
import psycopg2
from decouple import config
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

db_host = config("DB_HOST")
db_port = config("DB_PORT")
db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")

DB_CONNECTION_MAX_ATTEMPTS = 3
DB_CONNECTION_ATTEMPT = 0

while DB_CONNECTION_ATTEMPT < DB_CONNECTION_MAX_ATTEMPTS:
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("INFO:\t  Connection to the database established successfully.")
        break
    except (Exception, psycopg2.Error) as error:
        DB_CONNECTION_ATTEMPT += 1
        if DB_CONNECTION_ATTEMPT < DB_CONNECTION_MAX_ATTEMPTS:
            print(f"INFO:\t  DB connection attempt {DB_CONNECTION_ATTEMPT} failed.\
                   Retrying in 5 seconds...")
            time.sleep(5)
        else:
            break

if DB_CONNECTION_ATTEMPT == DB_CONNECTION_MAX_ATTEMPTS:
    print(f"INFO:\t  DB connection attempt {DB_CONNECTION_ATTEMPT} failed.")
    print("ERROR:\t  Max connection attempts reached. Aborting operation.")
    sys.exit(1)

products = []

class Product(BaseModel):
    """
    Represents a product with various attributes.

    Attributes:
        id (int): The product's unique identifier.
        number (str): The product's number.
        name (str, optional): The name of the product (optional).
        description (str, optional): The product's description (optional).
        revision (str): The product's revision.
        track (str): The product's track, default is 'main'.
    """
    id: Optional[int] = 0
    number: str
    name: Optional[str] = None
    description: Optional[str] = None
    revision: str
    track: str = "main"

def find_product(key, value):
    """
    Find a product by a specific key and value in the product list.

    Args:
        key (str): The key to search for (e.g., 'id' or 'revision').
        value: The value to search for.

    Returns:
        dict or None: The product matching the key and value, or None if not found.
    """
    for p in products:
        if p[key] == value:
            return p
    return None

@app.get("/")
def root():
    """
    Root endpoint. Returns a simple "Hello World" message.

    Returns:
        dict: A JSON response with a greeting message.
    """
    return {"message": "Hello World"}

@app.get("/products")
def get_products():
    """
    Retrieve all products from the database.

    Returns:
        list: A list of product records.
    """
    cursor.execute("SELECT * FROM products")
    products.append(cursor.fetchall())
    #for record in cursor:
    #    products.append(record)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products in the database."
        )
    return products

@app.get("/products/latest")
def get_latest_product():
    """
    Get the latest product from the product list.

    Returns:
        dict: The latest product.
    """
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products in the database."
        )
    product = products[-1]
    return product

@app.get("/products/revision={value}")
def get_product_by_revision(value):
    """
    Get a product by its revision.

    Args:
        value: The revision value to search for.

    Returns:
        dict: The product with the specified revision.
    """
    product = find_product("revision", value)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with revision {value} was not found."
        )
    return product

@app.get("/products/id={value}")
def get_product_by_id(value: int):
    """
    Get a product by its ID.

    Args:
        value (int): The ID to search for.

    Returns:
        dict: The product with the specified ID.
    """
    product = find_product("id", value)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {value} was not found."
        )
    return product

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(new_product: Product):
    """
    Create a new product and add it to the product list.

    Args:
        new_product (Product): The product to be created.

    Returns:
        list: The updated list of products with the new product added.
    """
    new_product_dict = new_product.dict()
    if new_product_dict["id"] == 0:
        new_product_dict["id"] = randrange(1, 100)
    products.append(new_product_dict)
    return products

@app.delete("/products/revision={value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_revision(value):
    """
    Delete a product by its revision.

    Args:
        value: The revision value to search for.

    Returns:
        None
    """
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
    """
    Delete a product by its ID.

    Args:
        value (int): The ID to search for.

    Returns:
        None
    """
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
    """
    Update a product by its revision.

    Args:
        revision: The revision of the product to be updated.
        change_product (Product): The updated product information.

    Returns:
        dict: The updated product information.
    """
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
