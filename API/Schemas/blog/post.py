from pydantic import BaseModel
from pydantic import Field

class Post(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI JWT",
                "content": "JWT SECURE!"
            }
        }