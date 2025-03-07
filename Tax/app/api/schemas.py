from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ Schema for Creating a Tax Entry
class TaxCreate(BaseModel):
    name: str
    type: str  # "Percentage" or "Fixed"
    value: float

# ✅ Schema for Updating a Tax Entry
class TaxUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None

# ✅ Schema for Tax Response
class TaxResponse(BaseModel):
    id: int
    name: str
    type: str
    value: float
    created_at: datetime
    updated_at: datetime
