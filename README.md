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

## Runing Application

You can now run the FastAPI application using the following command:

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI development server, and you can access the app in your browser at http://localhost:8000.

## Usage

The API provides the following endpoints:

    /products: Get a list of all products.
    /products/latest: Get the latest product.
    /products/revision={value}: Get a product by its revision.
    /products/id={value}: Get a product by its ID.
    /products: Create a new product (POST request).
    /products/revision={value}: Delete a product by its revision (DELETE request).
    /products/id={value}: Delete a product by its ID (DELETE request).
    /products/{revision}: Update a product by its revision (PUT request).

Refer to the script and comments for more details on the available routes and request payloads.

## Documentation
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. 

Make sure to create a `requirements.txt` file that lists the required packages for the project. It can be generated using `pip freeze` in the virtual environment, and it should include FastAPI and other dependencies used in the script.