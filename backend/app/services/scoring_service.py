import asyncio
import json
import logging
import os
import re
from pathlib import Path
from typing import List, Optional

import httpx

from app.models.candidate import CandidateResult, DetailedScores, ExtractedDocument
from app.utils.prompt_builder import build_cv_analysis_prompt

logger = logging.getLogger(__name__)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


MAX_CONCURRENT = max(1, min(4, _env_int("OLLAMA_MAX_CONCURRENT", 2)))


class LLMParseError(Exception):
    pass


class ScoringService:
    def __init__(self, base_url: str, model: str, timeout: float = 180.0):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout
        self._gpu_available: Optional[bool] = None
        self._gpu_probe_lock = asyncio.Lock()

    @property
    def model_name(self) -> str:
        return self._model

    async def check_connection(self):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self._base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                models = [m["name"] for m in data.get("models", []) if m.get("name")]
                self._select_available_model(models)
                return True, models
        except Exception:
            return False, []

    def _select_available_model(self, models: List[str]) -> None:
        if not models or self._model in models:
            return

        requested_base = self._model.split(":", 1)[0]
        for name in models:
            if name.split(":", 1)[0] == requested_base:
                self._model = name
                return

        logger.warning(
            "Configured Ollama model '%s' was not found. Using '%s'.",
            self._model,
            models[0],
        )
        self._model = models[0]

    async def _call_ollama(self, prompt: str) -> str:
        gpu_setting = os.getenv("OLLAMA_NUM_GPU", "auto").strip().lower()
        base_options = {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_predict": _env_int("OLLAMA_NUM_PREDICT", 260),
            "num_ctx": _env_int("OLLAMA_NUM_CTX", 4096),
        }

        if gpu_setting == "auto":
            if self._gpu_available is False:
                return await self._post_generate(prompt, {**base_options, "num_gpu": 0})

            if self._gpu_available is True:
                return await self._post_generate(prompt, base_options)

            async with self._gpu_probe_lock:
                if self._gpu_available is False:
                    return await self._post_generate(prompt, {**base_options, "num_gpu": 0})
                if self._gpu_available is True:
                    return await self._post_generate(prompt, base_options)

                try:
                    response = await self._post_generate(prompt, base_options)
                    self._gpu_available = True
                    return response
                except httpx.HTTPStatusError as exc:
                    if not self._is_gpu_runtime_error(exc):
                        raise
                    self._gpu_available = False
                    logger.warning("Ollama GPU runtime failed; using CPU for this analysis run.")
                    return await self._post_generate(prompt, {**base_options, "num_gpu": 0})

        return await self._post_generate(
            prompt,
            {**base_options, "num_gpu": _env_int("OLLAMA_NUM_GPU", 0)},
        )

    async def _post_generate(self, prompt: str, options: dict) -> str:
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": options,
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                f"{self._base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            return response.json().get("response", "")

    def _is_gpu_runtime_error(self, exc: httpx.HTTPStatusError) -> bool:
        try:
            body = exc.response.text.lower()
        except Exception:
            return False
        return any(token in body for token in ("cuda", "gpu", "vulkan", "device kernel image"))

    def _parse_llm_response(self, raw: str, filename: str) -> dict:
        cleaned = re.sub(r"```(?:json)?", "", raw.strip()).strip()

        for candidate in (cleaned, self._extract_json_object(cleaned)):
            if not candidate:
                continue
            parsed = self._try_load_json(candidate)
            if parsed is not None:
                return parsed

        raise LLMParseError(
            f"No JSON object found in LLM response for '{filename}'. Raw: {cleaned[:300]}"
        )

    def _try_load_json(self, value: str) -> Optional[dict]:
        variants = [
            value,
            re.sub(r",\s*([}\]])", r"\1", value),
            value.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'"),
        ]

        for variant in variants:
            try:
                parsed = json.loads(variant)
                if isinstance(parsed, list) and parsed:
                    parsed = parsed[0]
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                continue
        return None

    def _extract_json_object(self, text: str) -> str:
        start = text.find("{")
        if start < 0:
            return ""

        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(text)):
            char = text[idx]
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : idx + 1]

        return ""

    def _normalize_score(self, value) -> int:
        try:
            score = int(float(str(value).strip()))
        except (TypeError, ValueError):
            return 50
        return max(1, min(100, score))

    def _build_candidate_result(self, parsed: dict, filename: str, rank: int) -> CandidateResult:
        name = (
            parsed.get("candidateName")
            or parsed.get("candidate_name")
            or parsed.get("name")
            or self._candidate_name_from_filename(filename)
        )

        scores_raw = parsed.get("scores", {})
        if not scores_raw:
            scores_raw = parsed

        scores = DetailedScores(
            universityAndDepartment=self._normalize_score(
                scores_raw.get("universityAndDepartment")
                or scores_raw.get("university_and_department")
                or scores_raw.get("education")
                or scores_raw.get("educationScore")
                or 50
            ),
            foreignLanguages=self._normalize_score(
                scores_raw.get("foreignLanguages")
                or scores_raw.get("foreign_languages")
                or scores_raw.get("languages")
                or scores_raw.get("languageScore")
                or 50
            ),
            projects=self._normalize_score(
                scores_raw.get("projects")
                or scores_raw.get("projectExperience")
                or scores_raw.get("project_score")
                or 50
            ),
            internships=self._normalize_score(
                scores_raw.get("internships")
                or scores_raw.get("internshipExperience")
                or scores_raw.get("sectorExperience")
                or 50
            ),
            aiCompetency=self._normalize_score(
                scores_raw.get("aiCompetency")
                or scores_raw.get("ai_competency")
                or scores_raw.get("ai")
                or scores_raw.get("aiScore")
                or 50
            ),
        )

        return CandidateResult(
            rank=rank,
            candidateName=str(name).strip() or self._candidate_name_from_filename(filename),
            pdfFileName=filename,
            detailedScores=scores,
            averageScore=scores.average(),
            shortEvaluation=self._build_short_evaluation(scores),
        )

    def _candidate_name_from_filename(self, filename: str) -> str:
        stem = Path(filename).stem
        if stem.lower().startswith("cv_"):
            stem = stem[3:]
        return " ".join(part.capitalize() for part in re.split(r"[_\-\s]+", stem) if part)

    def _candidate_name_from_text(self, doc: ExtractedDocument) -> str:
        first_line = next((line.strip() for line in doc.text.splitlines() if line.strip()), "")
        if 2 <= len(first_line) <= 80 and not re.search(r"[@|:/\\]", first_line):
            return first_line
        return ""

    def _count_terms(self, text: str, terms: List[str]) -> int:
        return sum(1 for term in terms if term in text)

    def _build_short_evaluation(self, scores: DetailedScores) -> str:
        average = scores.average()
        strengths = []

        if scores.aiCompetency >= 85:
            strengths.append("yapay zeka yetkinliği")
        if scores.projects >= 85:
            strengths.append("proje deneyimi")
        if scores.universityAndDepartment >= 85:
            strengths.append("eğitim geçmişi")
        if scores.foreignLanguages >= 85:
            strengths.append("yabancı dil seviyesi")
        if scores.internships >= 85:
            strengths.append("staj ve sektör deneyimi")

        if average >= 85:
            if len(strengths) >= 2:
                return f"Aday {strengths[0]} ve {strengths[1]} alanlarında güçlü bir profil sunuyor."
            return "Aday genel değerlendirme kriterlerinde güçlü ve dengeli bir profil sunuyor."

        if average >= 70:
            if strengths:
                return f"Aday {strengths[0]} açısından öne çıkıyor; diğer kriterler rol beklentilerine göre değerlendirilebilir."
            return "Aday temel kriterlerde yeterli bir profil sunuyor; detaylı görüşmede teknik derinlik değerlendirilebilir."

        return "Adayda bazı olumlu göstergeler bulunuyor; ancak profilin rol beklentileriyle uyumu detaylı görüşmede netleştirilmelidir."

    def _score_by_profile(self, doc: ExtractedDocument) -> CandidateResult:
        text = doc.text
        lower = text.lower()

        university_terms = [
            "metu",
            "middle east technical",
            "bilkent",
            "boğaziçi",
            "bogazici",
            "koç",
            "koc",
            "istanbul technical",
            "itu",
            "sabancı",
            "sabanci",
        ]
        department_terms = [
            "computer engineering",
            "software engineering",
            "computer science",
            "electrical",
            "computational science",
        ]
        education = 45
        education += 18 if self._count_terms(lower, university_terms) else 0
        education += 22 if self._count_terms(lower, department_terms) else 0
        education += 7 if any(term in lower for term in ["m.sc", "master", "honors", "high honors"]) else 0
        education += 8 if re.search(r"gpa:\s*3\.[7-9]", lower) else 0

        language = 20
        if re.search(r"english.*(c2|proficient|toefl ibt 11)", lower):
            language = 94
        elif re.search(r"english.*(c1|advanced|ielts [78]|toefl)", lower):
            language = 86
        elif re.search(r"english.*(b2|upper intermediate)", lower):
            language = 74
        elif re.search(r"english.*(b1|intermediate)", lower):
            language = 55
        elif "english" in lower:
            language = 42
        language += min(10, 4 * len(re.findall(r"(german|french|spanish|italian|japanese|chinese)", lower)))

        project_terms = [
            "github",
            "open-source",
            "open sourced",
            "stars",
            "published",
            "kaggle",
            "rag",
            "benchmark",
            "pipeline",
            "extension",
            "platform",
        ]
        project_count = len(re.findall(r"\n[•\-]?\s*[A-Z][^\n:]{3,60}:", text))
        projects = 35 + min(35, project_count * 8) + min(25, self._count_terms(lower, project_terms) * 4)

        internship_count = len(re.findall(r"\bintern\b|\binternship\b", lower))
        internships = 18 + min(52, internship_count * 14)
        internships += min(
            25,
            self._count_terms(
                lower,
                [
                    "microsoft",
                    "aselsan",
                    "tubitak",
                    "tübitak",
                    "havelsan",
                    "vodafone",
                    "softtech",
                    "turkish airlines",
                ],
            )
            * 5,
        )

        ai_terms = [
            "pytorch",
            "tensorflow",
            "huggingface",
            "hugging face",
            "llm",
            "rag",
            "bert",
            "mlflow",
            "langchain",
            "llama",
            "mistral",
            "ollama",
            "opencv",
            "machine learning",
            "deep learning",
            "computer vision",
            "nlp",
            "sagemaker",
            "vertex ai",
        ]
        ai = 12 + min(82, self._count_terms(lower, ai_terms) * 7)

        scores = DetailedScores(
            universityAndDepartment=self._normalize_score(education),
            foreignLanguages=self._normalize_score(language),
            projects=self._normalize_score(projects),
            internships=self._normalize_score(internships),
            aiCompetency=self._normalize_score(ai),
        )

        first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
        name = first_line if 2 <= len(first_line) <= 80 else self._candidate_name_from_filename(doc.filename)

        return CandidateResult(
            rank=0,
            candidateName=name,
            pdfFileName=doc.filename,
            detailedScores=scores,
            averageScore=scores.average(),
            shortEvaluation=self._build_short_evaluation(scores),
        )

    async def _score_single_document(
        self, doc: ExtractedDocument, semaphore: asyncio.Semaphore
    ) -> Optional[CandidateResult]:
        async with semaphore:
            logger.info("Scoring '%s' with %s ...", doc.filename, self._model)
            try:
                prompt = build_cv_analysis_prompt(doc.text)
                raw_response = await self._call_ollama(prompt)
                logger.debug("Raw response for '%s': %s", doc.filename, raw_response[:400])
                parsed = self._parse_llm_response(raw_response, doc.filename)
                result = self._build_candidate_result(parsed, doc.filename, rank=0)
                result.candidateName = self._candidate_name_from_text(doc) or result.candidateName
                logger.info("Scored '%s' -> avg %.1f", doc.filename, result.averageScore)
                return result
            except httpx.TimeoutException:
                logger.error("Ollama timeout for '%s' (limit: %ss)", doc.filename, self._timeout)
                return self._score_by_profile(doc)
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                logger.error("Ollama request error for '%s': %s", doc.filename, exc)
                return self._score_by_profile(doc)
            except LLMParseError as exc:
                logger.error("%s", exc)
                return self._score_by_profile(doc)
            except Exception as exc:
                logger.error("Unexpected error for '%s': %s", doc.filename, exc)
                return self._score_by_profile(doc)

    async def score_documents(
        self, documents: List[ExtractedDocument], top_n: int = 5
    ) -> List[CandidateResult]:
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        tasks = [self._score_single_document(doc, semaphore) for doc in documents]
        results_raw = await asyncio.gather(*tasks)

        valid_results = [r for r in results_raw if r is not None]
        logger.info(
            "Scoring complete: %d/%d documents successfully scored.",
            len(valid_results),
            len(documents),
        )

        sorted_results = sorted(valid_results, key=lambda c: c.averageScore, reverse=True)
        top = sorted_results[:top_n]
        for idx, candidate in enumerate(top, start=1):
            candidate.rank = idx

        return top
