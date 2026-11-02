from uuid import UUID, uuid4
from fastapi import FastAPI, status
from app.schemas import StudySessionCreate, StudySessionRead

app = FastAPI(
    title="Study Session Organizer API",
    version="0.1.0",
)

sessions: dict[UUID, StudySessionRead] = {}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


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