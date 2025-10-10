"""
Pydantic models for API responses
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FileAction(BaseModel):
    """Represents a file operation"""
    source: str
    destination: str
    action_type: str = "move"  # move, copy, delete


class ScanResponse(BaseModel):
    """Response from scan/dry-run operation"""
    actions: List[FileAction]
    total_files: int
    message: str


class CleanResponse(BaseModel):
    """Response from clean operation"""
    processed: int
    success: bool
    message: str
    manifest_path: Optional[str] = None


class UndoResponse(BaseModel):
    """Response from undo operation"""
    reverted: int
    success: bool
    message: str


class HistoryEntry(BaseModel):
    """Single history entry"""
    timestamp: datetime
    operation: str  # clean, undo
    files_affected: int
    details: Optional[dict] = None


class HistoryResponse(BaseModel):
    """Response with operation history"""
    entries: List[HistoryEntry]
    total: int
