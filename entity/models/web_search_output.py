from pydantic import BaseModel, Field
from typing import Optional


class WebSearchOutputModel(BaseModel):
    """Pydantic model for the web rag search agent output"""
    product_name: Optional[str] = Field(None, alias="product_name")
    sku_id: Optional[str] = Field(None, alias="sku_id")