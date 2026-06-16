from pydantic import BaseModel
from typing import List, Optional
from app.models.candidate import CandidateResult


class AnalysisResponse(BaseModel):
    status: str
    processedCVCount: int
    topCandidates: List[CandidateResult]


class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    available_models: List[str]
    active_model: Optional[str] = None
