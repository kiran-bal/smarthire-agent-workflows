from pydantic import BaseModel, Field
from typing import Optional, List


class DiscountProcessorItemModel(BaseModel):
    """Pydantic model for the discount offer agent output"""
    item_no: Optional[str] = Field(None, alias="Item No.")
    s4_item_code: Optional[str] = Field(None, alias="S4 Item Code")
    item_description: Optional[str] = Field(None, alias="Item Description")
    sales_policy_group: Optional[str] = Field(None, alias="Sales Policy Group")
    brand: Optional[str] = Field(None, alias="Brand")
    inventory_uom: Optional[str] = Field(None, alias="Inventory UoM")
    chapter_id: Optional[str] = Field(None, alias="Chapter ID")
    mrp: Optional[float] = Field(None, alias="MRP")
    applied_offer: Optional[str] = Field(None, alias="Applied offer")
    discount_percentage: Optional[float] = Field(None, alias="Discount %")
    discounted_price: Optional[float] = Field(None, alias="Discounted price")

class DiscountProcessorModel(BaseModel):
    result: List[DiscountProcessorItemModel] = []