from collections.abc import Generator

from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    from app.database import engine

    with Session(engine) as db:
        yield db