from typing import Optional
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(prefix="/restaurant", tags=["Food Order API"])


class Order_details(BaseModel):
    item_name: str
    quantity: int
    price_per_item: float
    addons: Optional[List[str]] = []
    notes: Optional[str] = None


@router.post("/order/{restaurant_name}")
def create_order(restaurant_name: str, order: Order_details, delivery: bool = False):
    total_cost = order.quantity * order.price_per_item
    if delivery:
        total_cost += 40
    return {
        "restaurant": restaurant_name,
        "delivery": delivery,
        "item": order.item_name,
        "quantity": order.quantity,
        "total_cost": total_cost,
        "addons": order.addons,
        "notes": order.notes,
    }
