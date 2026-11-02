from datetime import datetime, timezone

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class StudySessionCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str = Field(min_length=1, max_length=100)
    course: str = Field(min_length=1, max_length=30)
    location: str = Field(min_length=1, max_length=200)
    starts_at: AwareDatetime
    capacity: int = Field(ge=2, le=50, strict=True)

    @field_validator("starts_at")
    @classmethod
    def validate_future_start(cls, value: datetime) -> datetime:
        if value <= datetime.now(timezone.utc):
            raise ValueError("Session start time must be in the future")
        return value