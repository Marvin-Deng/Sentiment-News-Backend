"""
Module defining Pydantic models for articles and response.
"""

from pydantic import BaseModel
from typing import List


class ResponseModel(BaseModel):
    message: str
    data: List
    status: int
