from pydantic import BaseModel, Field
from typing import Optional, Any


class EmailDraftOutputModel(BaseModel):
    """Pydantic model for the email draft agent output"""
    to: Optional[str] = Field(None, alias="To")
    subject: Optional[str] = Field(None, alias="Subject")
    message: Optional[Any] = Field(None, alias="Message")