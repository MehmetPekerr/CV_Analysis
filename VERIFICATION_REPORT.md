# Verification Report

Date: 2026-06-16

## Case Requirements

| Requirement | Status | Evidence |
| --- | --- | --- |
| At least 10 realistic software CVs in PDF format | Complete | `mock_cvs/` contains 10 generated PDF files |
| Multi-file PDF upload UI | Complete | `frontend/index.html` and `frontend/app.js` support multiple PDF selection and drag/drop |
| Backend PDF text extraction | Complete | `PDFService` extracts text with PyMuPDF and rejects empty/scanned content |
| Local Ollama model integration | Complete | Health endpoint detects `llama3:latest`; analysis endpoint calls Ollama |
| Five-criteria scoring | Complete | Scores returned for education, language, projects, internships, and AI competency |
| Average score calculation | Complete | Backend calculates arithmetic mean and rounds to one decimal |
| Top candidates sorted descending | Complete | Verified through `/api/v1/analyze?top_n=5` |
| Expected JSON response shape | Complete | Response contains `status`, `processedCVCount`, and `topCandidates` |
| Layered backend architecture | Complete | Controller, service, DTO, model, and utility layers are separated |
| Loading/error handling in UI | Complete | UI shows progress, Ollama status, errors, and empty-state handling |
| Tolerance for invalid model responses/timeouts | Complete | Backend falls back to evidence-based scoring if Ollama fails per document |

## PDF Validation

Checked all 10 mock CV PDFs:

- Each PDF opens successfully.
- Each PDF has extractable text.
- Turkish names render and extract correctly, including `Ayşe Kılıç`, `Furkan Doğan`, `Merve Yıldız`, `Selin Çelik`, and `Simge Aktaş`.
- No mojibake markers or replacement characters were found in extracted text.
- Rendered visual inspection showed no header overlap, clipped sections, or broken glyphs.

## API Validation

Health endpoint:

```json
{
  "status": "ok",
  "ollama_connected": true,
  "available_models": ["llama3:latest"],
  "active_model": "llama3:latest"
}
```

Full analysis test with 10 PDFs:

- HTTP status: `200`
- `processedCVCount`: `10`
- Returned candidates: `5`
- Rank order: descending by `averageScore`
- Score ranges: all values are integers between `1` and `100`
- Average score: verified against the five detailed scores

Representative top result:

```json
{
  "rank": 1,
  "candidateName": "Berk Kaya",
  "pdfFileName": "cv_berk_kaya.pdf",
  "averageScore": 89.6
}
```

## Environment Note

The local Ollama installation initially failed during generation with a CUDA runtime error. The backend is configured with `OLLAMA_NUM_GPU=auto`, so it tries the GPU runner first and retries on CPU if the local CUDA runtime fails. On a machine with a stable GPU setup, the same setting will use GPU acceleration without changing application code.

After updating the NVIDIA driver to `610.47`, Ollama loaded `llama3:latest` with GPU acceleration (`22%/78% CPU/GPU` reported by `ollama ps`). The full 10-PDF analysis completed successfully in about 64 seconds.

## Demo Note

For a live demo, start the services with `scripts/start_demo.ps1`, verify GPU usage with `ollama ps`, and use the provided 10 mock CVs for the most predictable result.
