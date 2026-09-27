from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):

    username: str
    email: str
    password: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):

    access_token: str
    token_type: str


class IncidentCreate(BaseModel):

    incident_type: str
    source: str
    severity: str
    description: Optional[str] = None

    failed_logins: int = 0
    request_count: int = 0
    connection_count: int = 0
    bytes_transferred: int = 0

class IncidentResponse(IncidentCreate):

    id: int
    risk_score: float
    status: str

    class Config:
        from_attributes = True

class IncidentStatusUpdate(BaseModel):

    status: str