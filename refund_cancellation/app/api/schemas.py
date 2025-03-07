from pydantic import BaseModel
from datetime import datetime

# ✅ Create Schema
class RefundCancellationCreate(BaseModel):
    title: str
    content: str

# ✅ Update Schema
class RefundCancellationUpdate(BaseModel):
    id: int
    title: str
    content: str

# ✅ Response Schema
class RefundCancellationResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime