from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ✅ Create Terms Schema
class TermsCreate(BaseModel):
    title: str
    content: str

# ✅ Update Terms Schema
class TermsUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None

# ✅ Response Schema
class TermsResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
