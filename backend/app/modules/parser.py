import re
import io
from PyPDF2 import PdfReader


class PDFParser:
    @staticmethod
    def extract_text(file_content: bytes) -> str:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text


class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s@.\-]', '', text)
        return text.strip()

    @staticmethod
    def segment_text(text: str) -> list:
        return [line.strip() for line in text.split('\n') if line.strip()]
