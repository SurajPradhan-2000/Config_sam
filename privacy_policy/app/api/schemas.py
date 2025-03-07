from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PrivacyPolicyCreate(BaseModel):
    title: str
    content: str


class PrivacyPolicyUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None


class PrivacyPolicyResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
