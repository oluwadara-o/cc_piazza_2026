# Create a post
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    body: str = Field(min_length=3, max_length=500)
    topics: Optional[List[str]] = Field(default=[])
    expires_at: datetime

class PostCreateResponse(BaseModel):
    post_id: int
    title: str = Field(min_length=3, max_length=500)
    topics: List[str] = Field(default=[])
    expires_at: datetime
    username: str

class PostBrowse(BaseModel):
    topic: Optional[str] = Field(default=None)

class PostBrowseSingleResponse(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    body: str = Field(min_length=3, max_length=500)
    expires_at: datetime

class PostBrowseResponse(BaseModel):
    posts: List[PostBrowseSingleResponse]