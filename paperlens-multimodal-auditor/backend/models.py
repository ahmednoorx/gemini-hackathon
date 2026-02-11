from pydantic import BaseModel, Field
from typing import List, Optional


class Claim(BaseModel):
    """Extracted claim from the paper."""
    text: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    page: int
    evidence_type: str  # "quantitative", "qualitative", "comparative"


class Contradiction(BaseModel):
    """Detected contradiction between text and visual evidence."""
    claim: str
    visual_evidence_page: int
    visual_shows: str  # Description of what the figure actually shows
    contradiction_type: str  # "direct_conflict", "partial_contradiction", "unsupported"
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: Optional[str] = None


class AuditReport(BaseModel):
    """Final audit report with detected contradictions."""
    claims: List[Claim]
    contradictions: List[Contradiction]
    audit_summary: str
    total_pages: int
    processing_time_seconds: float
    gemini_reasoning_trace: Optional[str] = None


class UploadResponse(BaseModel):
    """Response to file upload."""
    status: str  # "success", "error"
    message: str
    audit_report: Optional[AuditReport] = None
    error_details: Optional[str] = None
