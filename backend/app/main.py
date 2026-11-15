from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import StudySession
from app.schemas import StudySessionCreate, StudySessionRead


app = FastAPI(
    title="Study Session Organizer API",
    version="0.1.0",
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def readiness_check(db: DatabaseSession) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
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
def create_session(
    payload: StudySessionCreate,
    db: DatabaseSession,
) -> StudySessionRead:
    record = StudySession(**payload.model_dump())

    db.add(record)
    db.commit()
    db.refresh(record)

    return StudySessionRead.model_validate(record)


@app.get("/sessions", response_model=list[StudySessionRead])
def list_sessions(db: DatabaseSession) -> list[StudySessionRead]:
    statement = select(StudySession).order_by(
        StudySession.starts_at,
        StudySession.id,
    )
    records = db.scalars(statement).all()

    return [
        StudySessionRead.model_validate(record)
        for record in records
    ]