from fastapi import UploadFile
from fastapi import File
from pydantic import BaseModel
from fastapi import Form
from pydantic._internal import _model_construction
from fastapi import APIRouter, Response, status
from enum import Enum
from typing import Optional

router = APIRouter(prefix="/products", tags=["product"])


# Query Paramers
@router.get("/all")
def get_products(
    page: int = 1, category: Optional[str] = None, in_stock: Optional[bool] = True
):
    return {
        "message": f"Fetching products in category '{category}', in stock: {in_stock} on page {page}"
    }


@router.get("/search")
def search_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "price",
    order: Optional[str] = "asc",
    page: Optional[int] = 1,
    page_size: Optional[int] = 10,
):
    return {
        "message": f"Fetching products in category '{category}' with price between {min_price}-{max_price}, sorted by {sort_by} in {order} order, page {page} with {page_size} items per page"
    }


@router.post("/create")
def create_product(
    name: str = Form(...),
    brand_name: str = Form(...),
    price: Optional[float] = Form(...),
    image: UploadFile = File(...)
):
    return {
        "name": name,
        "brand_name": brand_name,
        "price": price,
        "image":image.filename,
        "message": "Product created successfully",
    }


## Sample example where we are taking data from the json instead of form
class ProductSchema(BaseModel):
    name: str
    price: int
    company_name: str


@router.post("/create-json")
def create_product_json(product: ProductSchema):
    return {
        "name": product.name,
        "brand_name": product.company_name,
        "price": product.price,
        "message": "Product created successfully",
    }
