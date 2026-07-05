from pydantic import Field
from fastapi import Path
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


class ProductReviewModel(BaseModel):
    username: str
    rating: int = Field(ge=1, le=5)
    comment: str


@router.post("/{product_id}")
def create_product(
    product_id: int = Path(
        ...,
        title="The Product ID",
        description="The unique identifier of the product",
        ge=1,
        le=5,
    ),
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


@router.post("/review/{product_category}")
def submit_review(
    product_category: str = Path(
        ...,
        title="The Product Category",
        description="The unique identifier of the product",
    ),
    min_price: float = Query(
        ..., gt=0, title="Minimum Price", description="The minimum price of the product"
    ),
    max_price: float = Query(
        ..., gt=0, title="Maximum Price", description="The maximum price of the product"
    ),
    user_reviews: List[ProductReviewModel] = [],
):
    return {
        "product_category": product_category,
        "price_range": {
            "min": min_price,
            "max": max_price,
        },
        "total_reviews": len(user_reviews),
        "reviews": user_reviews,
    }
