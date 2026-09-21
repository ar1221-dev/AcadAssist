from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from app.models.material import ProcessingStatus


class MaterialBase(BaseModel):
    title: str = Field(..., description="Document title")
    subject: str = Field(..., description="Academic subject/course")
    course: str | None = Field(default=None, description="Course code or identifier")
    description: str | None = Field(default=None, description="Optional description")


class MaterialResponse(BaseModel):
    id: str
    title: str
    original_filename: str
    filename: str
    file_type: str
    file_size: int
    content_hash: str
    subject: str
    course: str | None = None
    description: str | None = None
    processing_status: ProcessingStatus
    processing_error: str | None = None
    page_count: int | None = None
    slide_count: int | None = None
    content_length: int | None = None
    uploaded_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MaterialContentResponse(BaseModel):
    id: str
    title: str
    subject: str
    course: str | None = None
    file_type: str
    processing_status: ProcessingStatus
    content_length: int
    page_count: int | None = None
    slide_count: int | None = None
    processed_content: str
    
    model_config = ConfigDict(from_attributes=True)


class MaterialStatusResponse(BaseModel):
    id: str
    title: str
    processing_status: ProcessingStatus
    processing_error: str | None = None
    uploaded_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MaterialListResponse(BaseModel):
    total: int
    items: list[MaterialResponse]


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    context: dict[str, Any] | None = None
