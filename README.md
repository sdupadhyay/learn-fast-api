# 🚀 FastAPI Learning Journey & Revision Notes

Welcome to your FastAPI learning repository! This document serves as a comprehensive, easy-to-digest guide and cheat sheet for all the core FastAPI concepts you've practiced in this project.

---

## 📌 Table of Contents
1. [Project Setup & Running the App](#-project-setup--running-the-app)
2. [Application & Router Setup](#-1-application--router-setup)
3. [Path Parameters & Validation](#-2-path-parameters--validation)
4. [Query Parameters](#-3-query-parameters)
5. [Request Body & Pydantic Models](#-4-request-body--pydantic-models)
6. [Response Customization & Status Codes](#-5-response-customization--status-codes)

---

## 🛠 Project Setup & Running the App

Since this project is configured with `uv` and has a local virtual environment (`.venv`), you should always run the server using one of the following methods to ensure all dependencies (like `fastapi` and `uvicorn`) are loaded correctly.

### Method 1: Using `uv run` (Recommended)
```bash
uv run uvicorn main:app --reload
```

### Method 2: Activating the Virtual Environment
```bash
source .venv/bin/activate
uvicorn main:app --reload
```

> **Note:** The `--reload` flag tells Uvicorn to watch your files for changes and automatically restart the server when you save.

---

## 🧩 1. Application & Router Setup

Instead of putting all routes in a single `main.py` file, FastAPI allows you to modularize your code using **`APIRouter`**. This keeps your codebase clean and scalable.

### 📝 Key Concepts
*   **`FastAPI()`**: The core application class that binds everything.
*   **`APIRouter()`**: A mini-application class to group related routes (e.g., users, products).
*   **`prefix`**: Automatically prepends a path to all routes in the router.
*   **`tags`**: Categorizes routes in the auto-generated Swagger UI documentation (`/docs`).

### 💻 Code Example

**In `routers/user_get_routes.py`:**
```python
from fastapi import APIRouter

# Setup router with prefix and tags
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/all")
def get_all_user():
    return {"message": "All Users"}
```

**In `main.py`:**
```python
from fastapi import FastAPI
from routers import user_get_routes, product_routes, product_post

app = FastAPI()

# Include the routers into the main app
app.include_router(user_get_routes.router)
app.include_router(product_routes.router)
app.include_router(product_post.router)
```

---

## 🛣 2. Path Parameters & Validation

Path parameters are dynamic parts of the URL. They are defined using curly braces `{}` in the route decorator and must match the function argument names.

### 📝 Key Concepts
*   **Type Hinting**: FastAPI automatically parses and validates the type (e.g., `userName: str`, `product_id: int`). If the type doesn't match, it returns a `422 Unprocessable Entity` error automatically.
*   **Enum Validation**: You can restrict path parameter values to a specific set using Python's `Enum`.

### 💻 Code Example

#### Basic Path Parameter
```python
@router.get("/{userName}")
def get_userName(userName: str):
    return {"message": f"The user name is {userName}"}
```

#### Path Parameter restricted by Enums
```python
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    editor = "editor"
    viewer = "viewer"

# FastAPI will only accept /user/role/admin, /user/role/editor, or /user/role/viewer
@router.get("/role/{role}")
def get_user(role: UserRole):
    return {"message": f"The user role is {role.value}"}
```

---

## 🔍 3. Query Parameters

Query parameters are key-value pairs that appear after the `?` in the URL (e.g., `/products?page=2&category=electronics`). Any function arguments that are **not** part of the path path parameters are automatically treated as query parameters.

### 📝 Key Concepts
*   **Default Values**: Assigning a value (like `page: int = 1`) makes the parameter optional and provides a default.
*   **Optional Parameters**: Use `Optional[Type] = None` from the `typing` module to make a parameter completely optional.
*   **Query List Validation**: Use `Query(...)` to declare required query parameters or collections.

### 💻 Code Example

```python
from typing import Optional, List
from fastapi import Query

@router.get("/all")
def get_products(
    page: int = 1,                         # Optional with default 1
    category: Optional[str] = None,         # Completely optional
    in_stock: Optional[bool] = True        # Optional with default True
):
    return {"page": page, "category": category, "in_stock": in_stock}

# Query parameter expecting a list: /products/search?versions=v1&versions=v2
@router.get("/search")
def search_products(
    versions: List[str] = Query(...)       # '...' means it is REQUIRED
):
    return {"versions": versions}
```

---

## 📦 4. Request Body & Pydantic Models

To receive JSON data from the client, you use **Pydantic** models. Pydantic validates the structure and types of the incoming JSON.

### 📝 Key Concepts
*   **`BaseModel`**: The base class for defining schemas.
*   **`Body(...)`**: Used to declare a single, raw body parameter with validation rules (like `min_length`, `max_length`).

### 💻 Code Example

```python
from pydantic import BaseModel
from fastapi import Body
from typing import Optional

# Define the schema for the request body
class ProductModel(BaseModel):
    name: str
    price: int

@router.post("/{product_id}")
def create_product(
    product_id: int,                       # Path Parameter
    in_stock: Optional[bool] = True,       # Query Parameter
    product: ProductModel = None,          # Request Body (JSON)
    content: str = Body(..., min_length=5, max_length=15) # Singular Body Field
):
    return {
        "product_id": product_id,
        "product_details": product,
        "content": content
    }
```

---

## 🚦 5. Response Customization & Status Codes

You can dynamically set HTTP status codes (like `200 OK`, `201 Created`, `404 Not Found`) by injecting the `Response` object or utilizing FastAPI's `status` module.

### 📝 Key Concepts
*   **`Response`**: Injecting `response: Response` allows you to modify the status code or headers of the response dynamically.
*   **`status` Module**: Contains human-readable constants for HTTP status codes (e.g., `status.HTTP_200_OK`).

### 💻 Code Example

```python
from fastapi import Response, status

@router.get("/{userName}")
def get_userName(userName: str, response: Response):
    if userName == "sdupadhyay":
        response.status_code = status.HTTP_200_OK
        return {"message": f"Welcome back, {userName}!"}
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "User not found"}
```

---

## 📖 Quick Reference Cheat Sheet

| Feature | Syntax Example | Use Case |
| :--- | :--- | :--- |
| **Path Parameter** | `/items/{item_id}` | Identifying a specific resource. |
| **Query Parameter** | `/items?limit=10` | Filtering, sorting, or paginating results. |
| **Request Body** | `item: ItemModel` | Creating or updating resources with structured JSON. |
| **Enum Parameter** | `role: UserRole` | Restricting inputs to a specific set of options. |
| **Status Code** | `response.status_code = 404` | Indicating the outcome of the request. |
| **Body Validation** | `Body(..., min_length=5)` | Enforcing validation constraints on raw inputs. |

---

*Keep this notes file updated as you learn more advanced concepts like Dependency Injection, Database Integration (SQLAlchemy), and Authentication!* 😄
