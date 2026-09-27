from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )


class Incident(Base):

    __tablename__ = "incidents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_type = Column(
        String,
        nullable=False
    )

    source = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    failed_logins = Column(
        Integer,
        default=0
    )

    request_count = Column(
        Integer,
        default=0
    )

    connection_count = Column(
        Integer,
        default=0
    )

    bytes_transferred = Column(
        Integer,
        default=0
    )

    risk_score = Column(
        Float,
        default=0.0
    )

    status = Column(
        String,
        default="Open"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )