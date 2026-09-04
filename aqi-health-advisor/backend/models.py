from pydantic import BaseModel, Field
from typing import List
class ProfileIn(BaseModel):
    age_group: str = "18-39"
    medical_history: List[str] = Field(default_factory=list)
    occupation: str = ""
class AdvisoryRequest(BaseModel):
    lat: float
    lon: float
    profile: ProfileIn | None = None
