from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, status
from app.schemas import StudySessionCreate, StudySessionRead
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title="Study Session Organizer API",
    version="0.1.0",
)

sessions: dict[UUID, StudySessionRead] = {}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health/ready")
def readiness_check() -> dict[str, str]:
    from app.database import engine

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None

    return {"status": "ready"}

@app.post(
    "/sessions",
    response_model=StudySessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_session(payload: StudySessionCreate) -> StudySessionRead:
    session = StudySessionRead(
        id=uuid4(),
        **payload.model_dump(),
    )
    sessions[session.id] = session
    return session


@app.get("/sessions", response_model=list[StudySessionRead])
def list_sessions() -> list[StudySessionRead]:
    return list(sessions.values())