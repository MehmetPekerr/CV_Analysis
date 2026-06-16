# CV Scoring and Filtering System

Full-stack CV analysis application for ranking software engineering candidates from PDF resumes. The system extracts text from uploaded CVs, evaluates candidates with a local Ollama model, calculates five-category scores, and returns the top candidates in the expected JSON format.

## Features

- Multi-file PDF upload from a clean HTML interface
- Backend PDF text extraction with PyMuPDF
- Local Ollama integration for CV evaluation
- Five scoring criteria:
  - universityAndDepartment
  - foreignLanguages
  - projects
  - internships
  - aiCompetency
- Average score calculation and descending ranking
- Robust handling for unreadable PDFs, empty files, model timeouts, and invalid model responses
- 10 generated mock CV PDFs with Turkish character support

## Requirements

- Python 3.10+
- Ollama installed and running
- A local Ollama model, for example `llama3:latest`

## Setup

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Install or verify the Ollama model:

```bash
ollama pull llama3
ollama list
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Start the application:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

For demos on Windows, the helper script can start both Ollama and the backend:

```powershell
.\scripts\start_demo.ps1
```

## Configuration

The backend can read configuration from `backend/.env`. A ready-to-use example is provided as `backend/.env.example`.

```bash
cd backend
copy .env.example .env
```

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TIMEOUT=240
OLLAMA_MAX_CONCURRENT=2
OLLAMA_NUM_GPU=auto
OLLAMA_NUM_CTX=4096
OLLAMA_NUM_PREDICT=260
```

`OLLAMA_NUM_GPU=auto` tries Ollama's default GPU runner first. If the local GPU runtime fails with a CUDA or device-kernel error, the backend retries that CV on CPU instead of failing the whole analysis. To force CPU mode, set `OLLAMA_NUM_GPU=0`.

## Generate Mock CVs

```bash
cd mock_cvs
python generate_cvs.py
```

The script creates 10 realistic PDF CVs in `mock_cvs/`. It embeds a Unicode TrueType font so Turkish names such as `Ayşe Kılıç`, `Furkan Doğan`, and `Merve Yıldız` render and extract correctly.

## API

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/v1/health` | Checks backend and Ollama status |
| GET | `/api/v1/models` | Lists available Ollama models |
| POST | `/api/v1/analyze?top_n=5` | Uploads and analyzes CV PDFs |
| GET | `/docs` | FastAPI Swagger UI |

Example response:

```json
{
  "status": "success",
  "processedCVCount": 10,
  "topCandidates": [
    {
      "rank": 1,
      "candidateName": "Furkan Doğan",
      "pdfFileName": "cv_furkan_dogan.pdf",
      "detailedScores": {
        "universityAndDepartment": 90,
        "foreignLanguages": 95,
        "projects": 85,
        "internships": 80,
        "aiCompetency": 95
      },
      "averageScore": 89.0,
      "shortEvaluation": "Aday güçlü eğitim, proje ve yapay zeka deneyimiyle öne çıkıyor."
    }
  ]
}
```

## Troubleshooting

If the UI shows that Ollama is offline, start Ollama and check the model list:

```bash
ollama serve
ollama list
```

If Ollama is connected but generation fails with a CUDA-related error, keep `OLLAMA_NUM_GPU=auto` or set `OLLAMA_NUM_GPU=0` in `backend/.env`.

If analysis takes too long on CPU, reduce `OLLAMA_NUM_PREDICT` or use a smaller local model such as `mistral`, then set:

```text
OLLAMA_MODEL=mistral
```

After updating NVIDIA drivers, restart Windows and verify GPU inference:

```powershell
.\scripts\check_ollama_gpu.ps1
```

You can also confirm GPU usage while a model is loaded:

```bash
ollama ps
```

The `PROCESSOR` column should show GPU usage, for example `22%/78% CPU/GPU`.
