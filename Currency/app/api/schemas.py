from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CurrencyCreate(BaseModel):
    currencyname: str
    country: str

class CurrencyUpdate(BaseModel):
    id: int
    currencyname: str
    country: str

class CurrencyResponse(BaseModel):
    id: int
    currencyname: str
    country: str
    createdat: datetime
    updatedat: datetime
