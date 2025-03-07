from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ✅ Create Business Pr
class BusinessProfileCreate(BaseModel):
    name: str
    email: EmailStr  
    logo: Optional[str] = None  
    address: str
    contact: str  


class BusinessProfileUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    logo: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None

# ✅ Response Model (Read-Only)
class BusinessProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    logo: Optional[str] = None
    address: str
    contact: str
    created_at: Optional[datetime] = None  
    updated_at: Optional[datetime] = None  

    