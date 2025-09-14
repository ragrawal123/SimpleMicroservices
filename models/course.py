from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, StringConstraints

CourseCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{2,6}\s?\d{3,4}$")]

class CourseBase(BaseModel):
    code: CourseCode = Field(
        ...,
        description="Department+number code (e.g., COMS4701).",
        json_schema_extra={"example": "COMS4701"},
    )
    title: str = Field(
        ...,
        description="Course title.",
        json_schema_extra={"example": "Artificial Intelligence"},
    )
    description: Optional[str] = Field(
        None,
        description="Optional course description.",
        json_schema_extra={"example": "Foundations of modern artificial intelligence."},
    )
    credits: int = Field(
        3, ge=0, le=6,
        description="Credits.",
        json_schema_extra={"example": 3},
    )
    start_date: Optional[date] = Field(
        None, description="Course start date (YYYY-MM-DD).",
        json_schema_extra={"example": "2025-09-03"},
    )
    end_date: Optional[date] = Field(
        None, description="Course end date (YYYY-MM-DD).",
        json_schema_extra={"example": "2025-12-15"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "COMS4701",
                    "title": "Artificial Intelligence",
                    "description": "Foundations of modern artificial intelligence.",
                    "credits": 3,
                    "start_date": "2025-09-03",
                    "end_date": "2025-12-15",
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: UUID = Field(default_factory=uuid4, description="Server-generated Course ID.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.utcnow(), description="Creation timestamp (UTC)."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.utcnow(), description="Last update timestamp (UTC)."
    )


class CourseUpdate(BaseModel):
    code: Optional[CourseCode] = Field(None, description="Department+number code.")
    title: Optional[str] = Field(None, description="Course title.")
    description: Optional[str] = Field(None, description="Course description.")
    credits: Optional[int] = Field(None, ge=0, le=6, description="Credits.")
    start_date: Optional[date] = Field(None, description="Course start date.")
    end_date: Optional[date] = Field(None, description="Course end date.")
