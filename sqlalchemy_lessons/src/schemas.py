from datetime import datetime
from typing import Optional

from models import WorkLoad
from pydantic import BaseModel, ConfigDict, field_validator


class WorkersAddDTO(BaseModel):  # Моделька для POST запроса
    username: str


class WorkersDTO(WorkersAddDTO):  # моделька для GET запроса
    id: int


class ResumeAddDTO(BaseModel):
    title: str
    compensation: str
    workload: WorkLoad
    worker_id: int


class ResumeDTO(ResumeAddDTO):
    id: int
    compensation: str
    created_at: datetime
    updated_at: datetime

    @field_validator("compensation", mode="before")
    @classmethod
    def convert_salary_to_str(cls, v):
        if v is None:
            return v
        else:
            return str(v)


class ResumeRelDTO(ResumeDTO):  # DTO - data transfer object - это пустышка для передачи данных
    worker: "WorkersDTO"


class WorkerRelDTO(WorkersDTO):
    resumes: list["ResumeDTO"]
