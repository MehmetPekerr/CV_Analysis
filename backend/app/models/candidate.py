from pydantic import BaseModel, Field


class DetailedScores(BaseModel):
    universityAndDepartment: int = Field(..., ge=1, le=100)
    foreignLanguages: int = Field(..., ge=1, le=100)
    projects: int = Field(..., ge=1, le=100)
    internships: int = Field(..., ge=1, le=100)
    aiCompetency: int = Field(..., ge=1, le=100)

    def average(self) -> float:
        values = [
            self.universityAndDepartment,
            self.foreignLanguages,
            self.projects,
            self.internships,
            self.aiCompetency,
        ]
        return round(sum(values) / len(values), 1)


class CandidateResult(BaseModel):
    rank: int
    candidateName: str
    pdfFileName: str
    detailedScores: DetailedScores
    averageScore: float
    shortEvaluation: str


class ExtractedDocument(BaseModel):
    filename: str
    text: str
    page_count: int
