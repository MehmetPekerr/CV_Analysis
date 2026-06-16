import logging
from typing import List

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from app.dto.response_dto import AnalysisResponse, HealthResponse
from app.services.pdf_service import CVExtractionError, PDFService
from app.services.scoring_service import ScoringService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["CV Analysis"])

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


def get_pdf_service() -> PDFService:
    return PDFService()


def _create_scoring_service() -> ScoringService:
    import os
    return ScoringService(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        model=os.getenv("OLLAMA_MODEL", "llama3"),
        timeout=float(os.getenv("OLLAMA_TIMEOUT", "240")),
    )


@router.get("/health", response_model=HealthResponse, summary="System health check")
async def health_check():
    service = _create_scoring_service()
    connected, models = await service.check_connection()
    return HealthResponse(
        status="ok" if connected and models else "degraded",
        ollama_connected=connected,
        available_models=models,
        active_model=service.model_name if connected and models else None,
    )


@router.get("/models", summary="List available Ollama models")
async def list_models():
    service = _create_scoring_service()
    connected, models = await service.check_connection()
    if not connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cannot reach Ollama. Make sure it is running on port 11434.",
        )
    return {"models": models}


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Upload CVs and rank top candidates",
)
async def analyze_cvs(
    files: List[UploadFile] = File(..., description="PDF CV files"),
    top_n: int = Query(
        default=5, ge=1, le=20, description="Number of top candidates to return"
    ),
):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files were uploaded.",
        )

    pdf_service = get_pdf_service()
    documents = []
    skipped: List[str] = []

    for upload in files:
        if upload.content_type not in ("application/pdf", "application/octet-stream"):
            skipped.append(f"{upload.filename}: Not a PDF file.")
            continue

        file_bytes = await upload.read()

        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            skipped.append(f"{upload.filename}: Exceeds 10 MB size limit.")
            continue

        if len(file_bytes) == 0:
            skipped.append(f"{upload.filename}: Empty file.")
            continue

        try:
            doc = pdf_service.extract_text(file_bytes, upload.filename)
            documents.append(doc)
        except CVExtractionError as exc:
            logger.warning("Extraction failed: %s", exc)
            skipped.append(str(exc))

    if not documents:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": "No valid CV content could be extracted.",
                "skipped": skipped,
            },
        )

    if skipped:
        logger.info("Skipped files: %s", skipped)

    scoring_service = _create_scoring_service()

    connected, models = await scoring_service.check_connection()
    if not connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Ollama is not reachable at the configured address. "
                "Please start Ollama and ensure the model is pulled."
            ),
        )
    if not models:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama is running, but no local model is installed. Run 'ollama pull llama3' or set OLLAMA_MODEL to an installed model.",
        )

    top_candidates = await scoring_service.score_documents(documents, top_n=top_n)

    return AnalysisResponse(
        status="success",
        processedCVCount=len(documents),
        topCandidates=top_candidates,
    )
