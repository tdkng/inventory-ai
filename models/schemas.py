# uses pydantic for defining schema

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Part(BaseModel):
    part_number: str = Field(..., description="The unique identifier for the part")
    description: Optional[str] = Field(..., description="A brief description of the part")
    unit_price: float = Field(..., description="The price per unit of the part")
    unit_of_measure: str = Field(..., description="The unit of measure for the part")
    lead_time_days: Optional[int] = Field(..., description="The lead time in days for the part")

# inventory endpoint
class InventoryPosition(BaseModel):
    part_number: str = Field(..., description="The unique identifier for the part")
    warehouse: str = Field(..., description="The warehouse where the part is stored")
    on_hand_qty: int = Field(..., description="The quantity of the part in warehouse")
    allocated_qty: int = Field(..., description="The quantity of the part allocated for orders")
    available_qty: int = Field(..., description="The quantity of the part available for new orders")
    last_updated: str = Field(..., description="The last updated timestamp for the inventory position")

# usage endpoint
class UsageRecord(BaseModel):
    part_number: str = Field(..., description="The unique identifier for the part")
    quantity_used: int = Field(..., description="The quantity of the part used")
    usage_date: str = Field(..., description="The date when the part was used")

# purchase orders endpoint
class PurchaseOrder(BaseModel):
    po_number: str = Field(..., description="The unique identifier for the purchase order")
    part_number: str = Field(..., description="The unique identifier for the part ordered")
    order_qty: int = Field(..., description="The quantity of the part ordered")
    order_date: str = Field(..., description="The date when the order was placed")
    customer: str = Field(..., description="The customer who purchased the part")