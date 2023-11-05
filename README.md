# FastAPI Product Management App

This is a simple FastAPI application for managing product information.

## Prerequisites

- Python 3.7 or later
- [pip](https://pip.pypa.io/en/stable/)

## Installation

### 1. Install Python

Make sure you have Python 3.7 or a later version installed. You can download the latest version of Python from the [official website](https://www.python.org/downloads/).

### 2. Set Up a Virtual Environment (Optional but recommended)

Using a virtual environment is a good practice to isolate your project dependencies. Here's how to set up a virtual environment:

```bash
# On Unix or MacOS
python3 -m venv venv

# On Windows
python -m venv venv
```

Activate the virtual environment:

```bash
# On Unix or MacOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
### 3. Install Required Packages

In your virtual environment, use pip to install the necessary packages from the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Configure the environment variables by creating a .env file in the project directory:

    DB_HOST=database_host i.e. "127.0.0.0".
    DB_PORT=db_port i.e. 5432.
    DB_NAME=database_name i.e. ProductData.
    DB_USER=database_username.
    DB_PASSWORD=database_password.

## Runing Application

You can now run the FastAPI application using the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Your FastAPI web service will be accessible at http://localhost:8000.

## Environment Variables

    - `DB_HOST`: Your database host i.e. "127.0.0.0".
    - `DB_PORT`: Your db port.
    - `DB_NAME`: Name of your database.
    - `DB_USER`: Your PostgreSQL database username.
    - `DB_PASSWORD`: Your PostgreSQL database password.

## API Endpoints

The API provides the following endpoints:

    - GET /products: Retrieve all products from the database.
    - GET /products/latest: Get the latest product.
    - GET /products/revision={value}: Get a product by its revision.
    - GET /products/id={value}: Get a product by its ID.
    - POST /products: Create a new product.
    - DELETE /products/revision={value}: Delete a product by its revision.
    - DELETE /products/id={value}: Delete a product by its ID.
    - PUT /products/{revision}: Update a product by its revision.

Refer to the script and comments for more details on the available routes and request payloads.

## Product Schema

A product is represented by the following attributes:

    - `id` (optional): The product's unique identifier.
    - `number`: The product's number.
    - `name` (optional): The name of the product.
    - `description` (optional): The product's description.
    - `revision`: The product's revision.
    - `track` (default: 'main'): The product's track.

## Documentation
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. 

Make sure to create a `requirements.txt` file that lists the required packages for the project. It can be generated using `pip freeze` in the virtual environment, and it should include FastAPI and other dependencies used in the script.