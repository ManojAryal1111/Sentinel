from pydantic import BaseModel
from typing import Literal

class AttackProbe(BaseModel):
    id: str
    category: str              
    vector: Literal["direct", "indirect"]
    payload: str
    success_signature: str    
    severity: Literal["critical", "high", "medium", "low"]
    description: str = ""