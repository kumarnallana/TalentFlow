from pydantic import ConfigDict, BaseModel
from datetime import datetime
from typing import Any


class JobAcceptedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    status: str = "queued"
    message: str = "File uploaded and processing queued."
    created_at: datetime = datetime.utcnow


class JobDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    status: str = "queued"
    target_skills: list[str] | None = None
    extracted_data: dict[str, Any] | None = None
    error_message: str | None = None
    created_at: datetime
