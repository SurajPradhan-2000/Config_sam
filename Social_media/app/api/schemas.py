from pydantic import BaseModel
from datetime import datetime

class SocialMediaCreate(BaseModel):
    platform: str
    link: str

class SocialMediaUpdate(BaseModel):
    id: int
    platform: str
    link: str

class SocialMediaResponse(BaseModel):
    id: int
    platform: str
    link: str
    created_at: datetime
    updated_at: datetime
