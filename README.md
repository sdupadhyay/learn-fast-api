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

### Method 3: Packages Needed for Security & Uploads
To install new dependencies like file upload processors, token signing utilities, and static file routers:
```bash
uv pip install python-multipart python-jose fastapi
# Or using standard pip:
pip install python-multipart python-jose[cryptography]
```

---

## 🧩 1. Application & Router Setup

Instead of putting all routes in a single `main.py` file, FastAPI allows you to modularize your code using **`APIRouter`**. This keeps your codebase clean and scalable.

*   **`FastAPI()`**: The core application class that binds everything.
*   **`APIRouter()`**: A mini-application class to group related routes (e.g., users, products).
*   **`prefix`**: Automatically prepends a path to all routes in the router.
*   **`tags`**: Categorizes routes in the auto-generated Swagger UI documentation (`/docs`).

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

To receive JSON data from the client, you use **Pydantic** models. Pydantic validates the structure and types of the incoming JSON.

---

## 📥 5. Form Data & File Uploads

FastAPI allows receiving Form fields instead of JSON, which is crucial for handling file uploads or standard HTML form submissions.

> [!IMPORTANT]
> To receive uploaded files or form fields, you **must** install `python-multipart`.

### 📝 Key Concepts
*   **`Form`**: Declares that the input parameter should be read from the HTML form data rather than JSON.
*   **`File`**: Declares a file parameter.
*   **`bytes` vs `UploadFile`**:
    *   **`bytes`**: Reads the entire file into memory as raw bytes. Best for small files (e.g., text, small images).
    *   **`UploadFile`**: Reads the file in chunks and buffers it to disk if it's too large, preserving system memory. Provides access to `filename`, `content_type`, and a file-like object `file`. Recommended for all general uploads.

### 💻 Code Example (`routers/handle_file.py`)

#### Option A: Reading file contents directly as `bytes`
```python
from fastapi import APIRouter, File

router = APIRouter(tags=["Handle File"], prefix="/file")

@router.post("/")
def get_file(file: bytes = File(...)):
    # Decode raw bytes into UTF-8 text and split by newlines
    content = file.decode("utf-8")
    content_lines = content.split("\n")
    return {"content": content_lines}
```

#### Option B: Uploading and saving a file locally (`UploadFile`)
```python
import shutil
from fastapi import APIRouter, File, UploadFile

@router.post("/upload")
def upload_file(upload_file: UploadFile = File(...)):
    # Define local path where the file should be saved
    path = f"uploaded_files/{upload_file.filename}"
    
    # Save the file using Python's open() and shutil to copy binary stream
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        
    return {"file_name": upload_file.filename}
```

---

## 🌐 6. HTTP Headers (Request & Response)

HTTP headers are used to pass metadata between the client and server.

*   **`Header`**: Declares a header parameter. FastAPI automatically maps snake_case variable names (like `custom_header`) to kebab-case HTTP headers (like `Custom-Header`).
*   **`Response`**: Injecting `response: Response` lets you add custom headers dynamically to the HTTP response.

---

## ⏱ 7. Custom HTTP Middleware

Middleware is a function that runs before every request is processed by the path operations, and after every response is generated by the path operations.

### 📝 Key Concepts
*   **`@app.middleware("http")`**: Registers a function as an HTTP middleware.
*   **`call_next`**: A function that receives the `request` and passes it to the path operation, returning the generated `response`.

### 💻 Code Example (`main.py`)
```python
import time
from fastapi import Request

@app.middleware("http")
async def log_request(request: Request, call_next):
    # 1. Run code BEFORE the request goes to the router
    start_time = time.time()
    
    # 2. Forward the request to get the response
    response = await call_next(request)
    
    # 3. Run code AFTER the router finishes (e.g. calculate execution time)
    duration = time.time() - start_time
    print(f"Request: {request.url} | Time Taken: {duration:.4f} seconds")
    
    # 4. Return the response to the client
    return response
```

> [!NOTE]
> **Common Pitfall / Debugging Tip:** If you import time as `from time import time`, using `time.time()` will fail because `time` is now the float timestamp function directly, not the module. Use `start_time = time()` instead of `time.time()` if you imported it this way!

---

## 📂 8. Static Files Serving

FastAPI allows you to expose folders on your server so that static files (like uploaded images, stylesheets, or scripts) can be accessed directly from a URL.

### 📝 Key Concepts
*   **`StaticFiles`**: The class used to serve directory contents.
*   **`app.mount(url_path, StaticFiles(directory=...), name=...)`**: Mounts an independent sub-application to handle requests matching the `url_path`.

### 💻 Code Example (`main.py`)
```python
from fastapi.staticfiles import StaticFiles

# Expose the local "uploaded_files" directory at the "/files" path
# Example: Exposes "uploaded_files/pic.jpg" as "http://127.0.0.1:8000/files/pic.jpg"
app.mount("/files", StaticFiles(directory="uploaded_files"), name="files")
```

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
| **Bytes File** | `file: bytes = File(...)` | Reads whole file directly into memory as bytes (Text/CSV). |
| **UploadFile** | `upload_file: UploadFile = File(...)` | Streams files (handles large files safely, metadata access). |
| **File Buffer Copy** | `shutil.copyfileobj(file1, file2)` | Copies a binary file stream buffer efficiently. |
| **Mount Static Directory** | `app.mount("/url", StaticFiles(dir="path"))` | Exposes a folder directory at a specified public URL path. |
| **HTTP Middleware** | `@app.middleware("http")` | Intercepts requests/responses for logging, timing, etc. |
| **Next Middleware Call** | `response = await call_next(request)` | Forwards request to the path operations. |
| **CORS Middleware** | `CORSMiddleware` | Enables cross-origin requests from frontends. |

---

*Keep this notes file updated as you learn more advanced database concepts like Migrations (Alembic), OAuth2 scopes, and database optimization!* 😄
