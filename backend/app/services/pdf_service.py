import fitz
from app.models.candidate import ExtractedDocument


class CVExtractionError(Exception):
    pass


class PDFService:
    MIN_TEXT_LENGTH = 80

    def extract_text(self, file_bytes: bytes, filename: str) -> ExtractedDocument:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
        except Exception as exc:
            raise CVExtractionError(
                f"'{filename}' could not be opened as a valid PDF."
            ) from exc

        if doc.page_count == 0:
            raise CVExtractionError(f"'{filename}' contains no pages.")

        pages_text: list[str] = []
        for page in doc:
            pages_text.append(page.get_text("text"))

        full_text = "\n".join(pages_text).strip()

        if len(full_text) < self.MIN_TEXT_LENGTH:
            raise CVExtractionError(
                f"'{filename}' has insufficient text content (may be a scanned/image-only PDF)."
            )

        return ExtractedDocument(
            filename=filename,
            text=full_text,
            page_count=doc.page_count,
        )
