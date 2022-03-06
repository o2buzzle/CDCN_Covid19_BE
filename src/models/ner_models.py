from lib2to3.pytree import Base
import fastapi
from pydantic import BaseModel


class TextUpload(BaseModel):
    """
    Plain text for NER
    """

    text: str


class SingleWord(BaseModel):
    """
    A single word
    """

    token: str
    prediction: str
