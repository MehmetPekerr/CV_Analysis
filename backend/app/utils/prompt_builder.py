CV_ANALYSIS_PROMPT = """You are a senior technical recruiter for software engineering roles.

Analyze the CV text and score only the evidence present in the document. Return one valid JSON object and no other text.

CV TEXT:
---
{cv_text}
---

Return this exact JSON structure with integer scores between 1 and 100:
{{
  "candidateName": "<full name extracted from CV>",
  "scores": {{
    "universityAndDepartment": <integer 1-100>,
    "foreignLanguages": <integer 1-100>,
    "projects": <integer 1-100>,
    "internships": <integer 1-100>,
    "aiCompetency": <integer 1-100>
  }}
}}

Criteria:
- universityAndDepartment: university quality, department relevance, GPA or academic honors.
- foreignLanguages: English level first, then additional languages.
- projects: project depth, open-source/GitHub evidence, production relevance.
- internships: number, relevance, duration, company quality.
- aiCompetency: ML/AI frameworks, LLM/RAG work, publications, AI projects.

Use the candidate's real name exactly as it appears in the CV. If evidence for a criterion is weak or missing, assign a conservative score instead of inventing experience.
All scores must be integers from 1 to 100."""


def build_cv_analysis_prompt(cv_text: str) -> str:
    truncated = cv_text[:3200] if len(cv_text) > 3200 else cv_text
    return CV_ANALYSIS_PROMPT.format(cv_text=truncated)
