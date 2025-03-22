from pydantic import BaseModel
from typing import Optional


class TextRequest(BaseModel):
    text: str
    language: Optional[str] = None  # Auto-detect if not provided
    correct_grammar: Optional[bool] = False
    reword: Optional[bool] = False
