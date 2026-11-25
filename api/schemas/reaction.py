from typing import Literal

from pydantic import BaseModel, Field


class ReactPost(BaseModel):
    reaction_type: Literal['like', 'dislike']

class ReactResponse(BaseModel):
    post_id: int
    reaction_type: Literal['like', 'dislike']