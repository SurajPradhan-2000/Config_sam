from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    message: str
    module: str
    action: str

class NotificationUpdate(BaseModel):
    id: int
    read: bool

class NotificationResponse(BaseModel):
    id: int
    message: str
    read: bool
    module: str
    action: str
    created_at: datetime
    updated_at: datetime
