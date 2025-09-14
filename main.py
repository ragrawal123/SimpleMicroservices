from __future__ import annotations

import socket
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID
import os

from fastapi import FastAPI, HTTPException, Query, Path

# Import the new models
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.enrollment import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate
from models.health import Health

from pydantic import BaseModel, Field

port = int(os.environ.get("FASTAPIPORT", 8000))

app = FastAPI(
    title="University Microservice",
    description="FastAPI service exposing courses and enrollments (plus a health endpoint).",
    version="0.2.0",
)

courses: Dict[UUID, CourseRead] = {}
enrollments: Dict[UUID, EnrollmentRead] = {}


# -------------------- Health --------------------
def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# -------------------- Courses --------------------
@app.get("/courses", response_model=list[CourseRead], tags=["courses"])
def list_courses() -> list[CourseRead]:
    """List all courses."""
    return list(courses.values())


@app.post("/courses", response_model=CourseRead, status_code=201, tags=["courses"])
def create_course(course: CourseCreate) -> CourseRead:
    """Create a new course."""
    crs = CourseRead(**course.model_dump())
    if crs.id in courses:
        raise HTTPException(status_code=400, detail="Course with this ID already exists")
    courses[crs.id] = crs
    return crs


@app.get("/courses/{course_id}", response_model=CourseRead, tags=["courses"])
def get_course(course_id: UUID = Path(..., description="Course ID (UUID).")) -> CourseRead:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


@app.put("/courses/{course_id}", response_model=CourseRead, tags=["courses"])
def update_course(course_id: UUID, patch: CourseUpdate) -> CourseRead:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    current = courses[course_id]
    updated = current.model_copy(
        update={k: v for k, v in patch.model_dump(exclude_unset=True).items() if v is not None}
    )
    updated.updated_at = datetime.utcnow()
    courses[course_id] = updated
    return updated


@app.delete("/courses/{course_id}", status_code=204, tags=["courses"])
def delete_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return None


# -------------------- Enrollments --------------------
@app.get("/enrollments", response_model=list[EnrollmentRead], tags=["enrollments"])
def list_enrollments() -> list[EnrollmentRead]:
    """List all enrollments."""
    return list(enrollments.values())


@app.post("/enrollments", response_model=EnrollmentRead, status_code=201, tags=["enrollments"])
def create_enrollment(enr: EnrollmentCreate) -> EnrollmentRead:
    """Create a new enrollment. (Optionally validate course/person existence in a real DB.)"""
    new_enr = EnrollmentRead(**enr.model_dump())
    if new_enr.id in enrollments:
        raise HTTPException(status_code=400, detail="Enrollment with this ID already exists")
    enrollments[new_enr.id] = new_enr
    return new_enr


@app.get("/enrollments/{enrollment_id}", response_model=EnrollmentRead, tags=["enrollments"])
def get_enrollment(enrollment_id: UUID = Path(..., description="Enrollment ID (UUID).")) -> EnrollmentRead:
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollments[enrollment_id]


@app.put("/enrollments/{enrollment_id}", response_model=EnrollmentRead, tags=["enrollments"])
def update_enrollment(enrollment_id: UUID, patch: EnrollmentUpdate) -> EnrollmentRead:
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    current = enrollments[enrollment_id]
    updated = current.model_copy(
        update={k: v for k, v in patch.model_dump(exclude_unset=True).items() if v is not None}
    )
    updated.updated_at = datetime.utcnow()
    enrollments[enrollment_id] = updated
    return updated


@app.delete("/enrollments/{enrollment_id}", status_code=204, tags=["enrollments"])
def delete_enrollment(enrollment_id: UUID):
    if enrollment_id not in enrollments:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    del enrollments[enrollment_id]
    return None



@app.get("/")
def root():
    return {"message": "Welcome to the Course/Enrollment API. See /docs for OpenAPI UI."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)