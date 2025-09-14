from __future__ import annotations

from typing import Optional, Literal
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

EnrollmentStatus = Literal["enrolled", "waitlisted", "dropped", "completed"]

class EnrollmentBase(BaseModel):
    course_id: UUID = Field(
        ...,
        description="Course ID",
        json_schema_extra={"example": "COMS4701"},
    )
    person_id: UUID = Field(
        ...,
        description="Student UNI.",
        json_schema_extra={"example": "ra3295"},
    )
    status: EnrollmentStatus = Field(
        "enrolled",
        description="Enrollment status.",
        json_schema_extra={"example": "enrolled"},
    )
    semester: str = Field(
        ...,
        description="Semester",
        json_schema_extra={"example": "Fall 2025"},
    )
    grade: Optional[str] = Field(
        None,
        description="Final letter grade if completed.",
        json_schema_extra={"example": "A+"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_id": "COMS4701",
                    "person_id": "ra3295",
                    "status": "enrolled",
                    "semester": "Fall 2025",
                    "grade": None,
                }
            ]
        }
    }


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: UUID = Field(default_factory=uuid4, description="Server-generated Enrollment ID.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow(), description="Creation timestamp (UTC)."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.utcnow(), description="Last update timestamp (UTC)."
    )


class EnrollmentUpdate(BaseModel):
    status: Optional[EnrollmentStatus] = Field(None, description="Updated enrollment status.")
    grade: Optional[str] = Field(None, description="Update letter grade.")
    semester: Optional[str] = Field(None, description="Update semester label.")
