from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StudySession(Base):
    __tablename__ = "study_sessions"

    __table_args__ = (
        CheckConstraint(
            "capacity >= 2 AND capacity <= 50",
            name="ck_study_sessions_capacity",
        ),
        CheckConstraint(
            "length(trim(title)) > 0",
            name="ck_study_sessions_title_not_blank",
        ),
        CheckConstraint(
            "length(trim(course)) > 0",
            name="ck_study_sessions_course_not_blank",
        ),
        CheckConstraint(
            "length(trim(location)) > 0",
            name="ck_study_sessions_location_not_blank",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(100))
    course: Mapped[str] = mapped_column(String(30))
    location: Mapped[str] = mapped_column(String(200))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    capacity: Mapped[int]