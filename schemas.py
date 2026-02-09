
from pydantic import BaseModel, Field
from typing import Optional

class QueryIn(BaseModel):
    text: str
    max_cost: Optional[float] = 0.05

class SwarmIn(BaseModel):
    query: str
    style: Optional[str] = "scholar"

class WebhookIn(BaseModel):
    url: str
