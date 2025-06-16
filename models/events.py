from pydantic import BaseModel, ConfigDict
from typing import List

class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config = ConfigDict(json_schema_extra={
        "example": [
            {
                "title": "FastAPI Book Launch",
                "image": "https://example.com/image.jpg",
                "description": "We will be discussing tyhe contents of the FastAPI book in this event",
                "tags": ["python", "fatapi", "book", "launch"],
                "location": "Google Meet"
            }
        ]
    })


