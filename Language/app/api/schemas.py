from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LanguageCreate(BaseModel):
    language: str
    country: str

class LanguageUpdate(BaseModel):
    id: int
    language: Optional[str] = None
    country: Optional[str] = None

class LanguageResponse(BaseModel):
    id: int
    language: str
    country: str
    createdat: datetime
    updatedat: datetime
