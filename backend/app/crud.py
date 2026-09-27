from sqlalchemy.orm import Session

from .models import Incident
from .schemas import IncidentCreate


def create_incident(
    db: Session,
    incident: IncidentCreate,
    risk_score: float
):

    db_incident = Incident(
        incident_type=incident.incident_type,
        source=incident.source,
        severity=incident.severity,
        description=incident.description,
        failed_logins=incident.failed_logins,
        request_count=incident.request_count,
        connection_count=incident.connection_count,
        bytes_transferred=incident.bytes_transferred,

        risk_score=risk_score
    )

    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    return db_incident


def get_incidents(db: Session):

    return (
        db.query(Incident)
        .order_by(Incident.created_at.desc())
        .all()
    )


def get_incident(
    db: Session,
    incident_id: int
):

    return (
        db.query(Incident)
        .filter(
            Incident.id == incident_id
        )
        .first()
    )


def delete_incident(
    db: Session,
    incident_id: int
):

    incident = get_incident(
        db,
        incident_id
    )

    if incident:

        db.delete(incident)
        db.commit()

    return incident
def update_incident_status(
    db: Session,
    incident_id: int,
    new_status: str
):

    incident = get_incident(
        db,
        incident_id
    )

    if incident:

        incident.status = new_status

        db.commit()

        db.refresh(incident)

    return incident