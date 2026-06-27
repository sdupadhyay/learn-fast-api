from pydantic._internal import _model_construction
from fastapi import APIRouter, Response,status
from enum import Enum
from typing import Optional
router = APIRouter(prefix="/products",tags=["product"])
# Query Paramers 
@router.get("/all")
def get_products(
    page: int = 1,
    category: Optional[str] = None,
    in_stock: Optional[bool] = True
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
    page_size: Optional[int] = 10
):
    return {
        "message": f"Fetching products in category '{category}' with price between {min_price}-{max_price}, sorted by {sort_by} in {order} order, page {page} with {page_size} items per page"
    }