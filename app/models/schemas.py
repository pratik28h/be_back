from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str
    preview: Optional[List[Dict[str, Any]]] = None
    rows: Optional[int] = None
    columns: Optional[List[str]] = None
    charts: Optional[List[str]] = None

# New Schemas for Frontend Alignment

class DataSourceMeta(BaseModel):
    filename: str
    rows: int
    column_count: int
    size: int
    uploaded_at: str

class DataSourceListResponse(BaseModel):
    files: List[DataSourceMeta]

class PreviewRequest(BaseModel):
    filename: str
    command: Optional[str] = None

class PreviewResponse(BaseModel):
    original_preview: List[Dict[str, Any]]
    preview: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    diff_summary: str

class PreprocessRequest(BaseModel):
    filename: str
    command: str

class PreprocessResponse(BaseModel):
    message: str
    rows: int
    columns: List[str]
    preview: List[Dict[str, Any]]
