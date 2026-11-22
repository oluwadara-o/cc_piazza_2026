# Create a post
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    body: str = Field(min_length=3, max_length=500)
    topics: Optional[List[str]] = Field(default=[])
    expires_at: datetime
    username: str