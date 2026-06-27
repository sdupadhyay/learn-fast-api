from fastapi import Query
from typing import List
from fastapi import Body
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["product"])


class ProductModel(BaseModel):
    name: str
    price: int


@router.post("/{product_id}")
def create_product(
    product_id: int,
    in_stock: Optional[bool] = True,
    product: ProductModel = None,
    content: str = Body(..., min_length=5, max_length=15),
    versions: List[str] = Query(...),
):
    return {
        "message": "Product updated successfully!",
        "product_id": product_id,
        "in_stock": in_stock,
        "product_details": product,
        "content": content,
        "List": versions,
    }
