from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
import hashlib

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    user_agent: Optional[str] = None
    comments: Optional[str] = Field(None, max_length=1000)
    submission_id: Optional[str] = None
  

    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v
        
    @validator("email")
    def hash_email(cls, v):
        """Hash email for PII protection"""
        return hashlib.sha256(str(v).encode()).hexdigest()
    
    @validator("age")
    def hash_age(cls, v):
        """Hash age for PII protection"""
        return hashlib.sha256(str(v).encode()).hexdigest()
    
    # Exercise 3: Generate submission_id if not provided
    @validator("submission_id", always=True)
    def generate_submission_id(cls, v, values):
        """Generate submission_id if not provided"""
        if v:  # If submission_id is already provided, keep it
            return v
        
        # Generate from hashed email + current date/hour
        email = values.get('email', '')
        if email:
            current_time = datetime.utcnow().strftime('%Y%m%d%H')
            combined = f"{email}{current_time}"
            return hashlib.sha256(combined.encode()).hexdigest()
        
        return None

#Good example of inheritance
class StoredSurveyRecord(BaseModel):
    received_at: datetime
    ip: str
    name: str 
    email: EmailStr
    age: int  
    consent: bool 
    rating: int 
    user_agent: Optional[str] = None
    comments: Optional[str] 
    submission_id: Optional[str] = None
