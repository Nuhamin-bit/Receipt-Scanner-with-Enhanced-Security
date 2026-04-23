"""
Receipt processing pipeline (CLEAN VERSION - Tesseract only)
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, List

from PIL import Image, UnidentifiedImageError
import pytesseract

# =========================
# RENDER / LOCAL FIX
# =========================

IS_RENDER = os.getenv("RENDER", False)

if IS_RENDER:
    TESSERACT_PATH = "/usr/bin/tesseract"
else:
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# =========================
# IMAGE PREPROCESSOR
# =========================

class ImagePreprocessor:
    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png"}

    def preprocess(self, image_path: str) -> str:
        path = Path(image_path)

        if not path.exists():
            raise ValueError("File not found")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError("Unsupported format")

        try:
            img = Image.open(path).convert("L")
            processed_path = path.with_name(f"{path.stem}_processed.png")
            img.save(processed_path)
            return str(processed_path)

        except Exception as e:
            raise RuntimeError(f"Image preprocessing failed: {e}")


# =========================
# OCR PROCESSOR
# =========================

class OCRProcessor:
    def extract_text(self, image_path: str) -> str:
        try:
            img = Image.open(image_path)

            config = "--oem 3 --psm 6"
            text = pytesseract.image_to_string(img, config=config)

            return text.strip()

        except UnidentifiedImageError:
            raise ValueError("Invalid image")
        except Exception as e:
            raise RuntimeError(f"OCR failed: {e}")


# =========================
# TEXT PARSER
# =========================

class TextProcessor:

    AMOUNT_REGEX = re.compile(r"\$([0-9]+\.?[0-9]*)")
    DATE_REGEX = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")

    def parse_text(self, text: str) -> Dict[str, Any]:

        lines = [l.strip() for l in text.splitlines() if l.strip()]

        total = self._extract_total(text)
        date = self._extract_date(text)
        merchant = lines[0] if lines else "Unknown"

        return {
            "merchant": merchant,
            "date": date,
            "total": total,
            "raw_text": text[:3000]
        }

    def _extract_total(self, text: str) -> Optional[str]:
        matches = self.AMOUNT_REGEX.findall(text)
        return max(matches, default=None)

    def _extract_date(self, text: str) -> Optional[str]:
        match = self.DATE_REGEX.search(text)
        return match.group(0) if match else None


# =========================
# MAIN SCANNER
# =========================

class ReceiptScanner:

    def __init__(self):
        self.pre = ImagePreprocessor()
        self.ocr = OCRProcessor()
        self.parser = TextProcessor()

    def parse_image(self, image_path: str) -> Dict[str, Any]:

        processed = self.pre.preprocess(image_path)
        text = self.ocr.extract_text(processed)

        return self.parser.parse_text(text)