from beanie import Document
from typing import Optional, List
from pydantic import ConfigDict, BaseModel


class Event(Document):
    creator: Optional[str] = None
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "title": "FastAPI Book Launch",
                    "image": "https://example.com/image.jpg",
                    "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                    "tags": ["python", "fatapi", "book", "launch"],
                    "location": "Google Meet",
                }
            ]
        }
    )

    class Settings:
        name = "events"


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "title": "FastAPI Book Launch",
                    "image": "https://example.com/image.jpg",
                    "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                    "tags": ["python", "fatapi", "book", "launch"],
                    "location": "Google Meet",
                }
            ]
        }
    )


# from pydantic import BaseModel, ConfigDict
# from typing import List

# class Event(BaseModel):
#    id: int
#    title: str
#    image: str
#    description: str
#    tags: List[str]
#    location: str

#    model_config = ConfigDict(json_schema_extra={
#        "example": [
#            {
#                "title": "FastAPI Book Launch",
#                "image": "https://example.com/image.jpg",
#                "description": "We will be discussing tyhe contents of the FastAPI book in this event",
#                "tags": ["python", "fatapi", "book", "launch"],
#                "location": "Google Meet"
#            }
#        ]
#    })
