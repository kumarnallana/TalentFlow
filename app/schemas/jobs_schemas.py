
from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime, timezone
from typing import Any, Annotated
from fastapi import Query


class JobAcceptedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    status: str = "queued"
    message: str = "File uploaded and processing queued."
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    status: str = "queued"
    target_skills: list[str] | None = None
    extracted_data: dict[str, Any] | None = None
    error_message: str | None = None
    created_at: datetime


class Pagination(BaseModel):

    skip: Annotated[
        int,
        Query(ge=0, description="Records to skip")
    ] = 0

    limit: Annotated[
        int,
        Query(gt=0, le=100, description="Records to fetch")
    ] = 10
