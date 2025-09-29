from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, validator
import hashlib

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool
    rating: int = Field(..., ge=1, le=5)
    user_agent: Optional[str] = None
    comments: Optional[str] = Field(None, max_length=1000)
    source: Literal["homepage", "email", "qr", "other"] = "other"
    submission_id: Optional[str] = None
  

    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v
        
       

#Good example of inheritance
class StoredSurveyRecord(BaseModel):
    received_at: datetime
    ip: str
    name: str 
    hashed_email: str
    hashed_age: str
    consent: bool 
    rating: int 
    user_agent: Optional[str] = None
    comments: Optional[str] = None
    source: Literal["homepage", "email", "qr", "other"] = "other"
    submission_id: str 
