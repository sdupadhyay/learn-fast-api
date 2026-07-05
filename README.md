# 🚀 FastAPI Learning Journey & Revision Notes

Welcome to your FastAPI learning repository! This document serves as a comprehensive, easy-to-digest guide and cheat sheet for all the core FastAPI concepts you've practiced in this project.

---

## 📌 Table of Contents
1. [Project Setup & Running the App](#-project-setup--running-the-app)
2. [Application & Router Setup](#-1-application--router-setup)
3. [Path Parameters & Validation](#-2-path-parameters--validation)
4. [Query Parameters](#-3-query-parameters)
5. [Request Body & Pydantic Models](#-4-request-body--pydantic-models)
6. [Form Data & File Uploads](#-5-form-data--file-uploads)
7. [HTTP Headers (Request & Response)](#-6-http-headers-request--response)
8. [Custom HTTP Middleware](#-7-custom-http-middleware)
9. [Static Files Serving](#-8-static-files-serving)
10. [CORS (Cross-Origin Resource Sharing)](#-9-cors-cross-origin-resource-sharing)
11. [Database Integration (SQLAlchemy ORM)](#-10-database-integration-sqlalchemy-orm)
12. [Security & Password Hashing](#-11-security--password-hashing)
13. [JWT (JSON Web Token) Authentication](#-12-jwt-json-web-token-authentication)
14. [Complete CRUD & Auth Reference](#-13-complete-crud--auth-reference)

---

## 🛠 Project Setup & Running the App

Since this project is configured with `uv` and has a local virtual environment (`.venv`), you should always run the server using one of the following methods to ensure all dependencies are loaded correctly.

### Method 1: Using `uv run` (Recommended)
```bash
uv run uvicorn main:app --reload
```

### Method 2: Activating the Virtual Environment
```bash
source .venv/bin/activate
uvicorn main:app --reload
```

---

## 🧩 1. Application & Router Setup

Instead of putting all routes in a single `main.py` file, FastAPI allows you to modularize your code using **`APIRouter`**. This keeps your codebase clean and scalable.

---

## 🛣 2. Path Parameters & Validation

Path parameters are dynamic parts of the URL. They are defined using curly braces `{}` in the route decorator and must match the function argument names.

*   **Type Hinting**: FastAPI automatically parses and validates the type (e.g., `userName: str`, `product_id: int`).
*   **Enum Validation**: Restricts path parameter values to a specific set using Python's `Enum`.
*   **`Path` Validation & Metadata**: You can use `Path` from `fastapi` to add metadata (like `title` and `description`) and numeric validation constraints:
    *   `gt`: Greater than
    *   `ge`: Greater than or equal to (e.g., `ge=1`)
    *   `lt`: Less than
    *   `le`: Less than or equal to (e.g., `le=5`)

---

## 🔍 3. Query Parameters

Query parameters are key-value pairs that appear after the `?` in the URL (e.g., `/products?page=2&category=electronics`). Any function arguments that are **not** part of the path path parameters are automatically treated as query parameters.

---

## 📦 4. Request Body & Pydantic Models

To receive JSON data from the client, you use **Pydantic** models. Pydantic validates the structure and types of the incoming JSON payloads.

### 📝 Key Concepts
*   **`BaseModel`**: The base class for defining schemas.
*   **`Body(...)`**: Used to declare a single, raw body parameter with validation rules.
*   **Nested Pydantic Models**: You can nest schemas inside other schemas.
*   **`Field` Validation**: You can use `Field` from `pydantic` to apply validation rules directly to schema attributes (e.g. `gt=0`, `ge=1`, `le=5`).
*   **Custom Field Validators (`@field_validator`)**: You can write custom functions to validate fields using complex logic or regex.

### 💻 Code Example

#### A. Basic Model & Body Parameter
```python
from pydantic import BaseModel
from fastapi import Body

class ProductModel(BaseModel):
    name: str
    price: int

@router.post("/{product_id}")
def create_product(
    product: ProductModel = None,
    content: str = Body(..., min_length=5, max_length=15)
):
    return {"product": product, "content": content}
```

#### B. Model Validation using `Field` and `@field_validator` (`schemas/booking_schema.py`)
```python
import re
from pydantic import BaseModel, Field, field_validator

class Booking(BaseModel):
    movie_name: str
    seats: int = Field(gt=0)                   # Seats must be greater than 0
    show_time: str                             # Expected HH:MM 24-hr format

    # Custom validator using @field_validator (Pydantic v2 style)
    @field_validator("show_time")
    @classmethod
    def validate_show_time(cls, value: str) -> str:
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", value):
            raise ValueError("show_time must be in HH:MM format (24-hour clock)")
        return value
```

#### C. Route Combining Path, Query, and Request Body (`routers/product_post.py`)
FastAPI allows you to combine multiple input sources (Path, Query, and Request Body) in a single request seamlessly.

```python
from fastapi import APIRouter, Path, Query
from typing import List
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["product"])

class ProductReviewModel(BaseModel):
    username: str
    rating: int = Field(ge=1, le=5)           # Rating must be between 1 and 5
    comment: str

@router.post("/review/{product_category}")
def submit_review(
    product_category: str = Path(             # 1. Path Parameter
        ...,
        title="Product Category"
    ),
    min_price: float = Query(..., gt=0),      # 2. Query Parameter (with gt validation)
    max_price: float = Query(..., gt=0),      # 2. Query Parameter
    user_reviews: List[ProductReviewModel] = [] # 3. Request Body (List of Models)
):
    return {
        "category": product_category,
        "price_range": {"min": min_price, "max": max_price},
        "reviews": user_reviews
    }
```

---

## 📥 5. Form Data & File Uploads

FastAPI allows receiving Form fields instead of JSON, which is crucial for handling file uploads or standard HTML form submissions.

---

## 🌐 6. HTTP Headers (Request & Response)

HTTP headers are used to pass metadata between the client and server.

---

## ⏱ 7. Custom HTTP Middleware

Middleware is a function that runs before every request is processed by the path operations, and after every response is generated by the path operations.

---

## 📂 8. Static Files Serving

FastAPI allows you to expose folders on your server so that static files (like uploaded images, stylesheets, or scripts) can be accessed directly from a URL.

---

## 🛡 9. CORS (Cross-Origin Resource Sharing)

If your frontend (e.g., React, Next.js) is hosted on a different domain or port than your FastAPI backend, the browser will block requests unless **CORS Middleware** is enabled.

---

## 🗄 10. Database Integration (SQLAlchemy ORM)

Integrating a database using an **Object Relational Mapper (ORM)** like **SQLAlchemy** allows you to interact with database tables using Python classes instead of writing raw SQL queries.

---

## 🔑 11. Security & Password Hashing

For security, you must **never** store passwords as plain text. Instead, hash them using a one-way hashing algorithm like `bcrypt`.

---

## 🎫 12. JWT (JSON Web Token) Authentication

FastAPI uses **OAuth2** flows for authentication. JSON Web Tokens (JWT) are signed tokens generated by the server and sent to the client upon login. The client stores the token and sends it in the `Authorization: Bearer <token>` header of subsequent API calls to access protected routes.

---

## 🔄 13. Complete CRUD & Auth Reference

Here is how to perform all CRUD (Create, Read, Update, Delete) and Authentication operations.

---

## 📖 Quick Reference Cheat Sheet

| Feature | Syntax / Method | Purpose |
| :--- | :--- | :--- |
| **Field Constraints** | `price: float = Field(gt=0)` | Apply numeric, length, or metadata rules directly to model fields. |
| **Custom Validator** | `@field_validator("field_name")` | Pydantic v2 decorator to implement custom checks (e.g. regex). |
| **Path parameter** | `Path(..., title="...")` | Adds constraints & metadata to URL path variables. |
| **Query parameter** | `Query(..., gt=0)` | Adds constraints & metadata to URL query parameters. |
| **Bytes File** | `file: bytes = File(...)` | Reads whole file directly into memory as bytes (Text/CSV). |
| **UploadFile** | `upload_file: UploadFile = File(...)` | Streams files (handles large files safely, metadata access). |
| **File Buffer Copy** | `shutil.copyfileobj(file1, file2)` | Copies a binary file stream buffer efficiently. |
| **Mount Static Directory** | `app.mount("/url", StaticFiles(dir="path"))` | Exposes a folder directory at a specified public URL path. |
| **HTTP Middleware** | `@app.middleware("http")` | Intercepts requests/responses for logging, timing, etc. |
| **Next Middleware Call** | `response = await call_next(request)` | Forwards request to the path operations. |
| **CORS Middleware** | `CORSMiddleware` | Enables cross-origin requests from frontends. |

---

*Keep this notes file updated as you learn more advanced database concepts like Migrations (Alembic), OAuth2 scopes, and database optimization!* 😄
