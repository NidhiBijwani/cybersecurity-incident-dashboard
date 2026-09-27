from fastapi.middleware.cors import CORSMiddleware

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .database import (
    Base,
    engine,
    get_db
)

from .models import User

from .schemas import (
    UserCreate,
    UserResponse,
    Token,
    IncidentCreate,
    IncidentResponse,
    IncidentStatusUpdate
)

from .crud import (
    create_incident,
    get_incidents,
    get_incident,
    delete_incident,
    update_incident_status
)

from .ml.detector import (
    AnomalyDetector,
    calculate_risk_score
)

from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Cybersecurity Incident Dashboard",
    description="API for managing and analyzing cybersecurity incidents.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
detector = AnomalyDetector()

@app.get("/")
def home():

    return {
        "message": "Cybersecurity Incident Dashboard API",
        "status": "running"
    }


# ----------------------------------
# REGISTER
# ----------------------------------

@app.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(
            user.password
        )
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ----------------------------------
# LOGIN
# ----------------------------------

@app.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.username == form_data.username
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(
        user.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ----------------------------------
# CURRENT USER
# ----------------------------------

@app.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user


# ----------------------------------
# CREATE INCIDENT
# ----------------------------------

@app.post(
    "/incidents",
    response_model=IncidentResponse
)
def add_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

   anomaly = detector.predict(
        failed_logins=incident.failed_logins,
        request_count=incident.request_count,
        connection_count=incident.connection_count,
        bytes_transferred=incident.bytes_transferred
    )
   risk_score = calculate_risk_score(
        incident.severity,
        anomaly
    )
   return create_incident(
        db,
        incident,
        risk_score
    )


# ----------------------------------
# GET INCIDENTS
# ----------------------------------

@app.get(
    "/incidents",
    response_model=list[IncidentResponse]
)
def list_incidents(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return get_incidents(db)


# ----------------------------------
# GET SINGLE INCIDENT
# ----------------------------------

@app.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse
)
def incident_details(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    incident = get_incident(
        db,
        incident_id
    )

    if not incident:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident

@app.patch(
    "/incidents/{incident_id}/status",
    response_model=IncidentResponse
)
def update_status(
    incident_id: int,
    status_update: IncidentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if status_update.status not in [
        "Open",
        "Closed"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Open or Closed"
        )

    incident = update_incident_status(
        db,
        incident_id,
        status_update.status
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident
# ----------------------------------
# DELETE INCIDENT
# ----------------------------------

@app.delete(
    "/incidents/{incident_id}"
)
def remove_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    incident = delete_incident(
        db,
        incident_id
    )

    if not incident:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "message": "Incident deleted successfully"
    }