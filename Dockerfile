FROM python:3.12-slim

# Keep Python predictable in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# System packages:
# - tesseract-ocr: OCR engine required by pytesseract
# - libglib2.0-0 / libsm6 / libxext6 / libxrender1: common Pillow runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the repository contents
COPY . .

# Fix package structure
RUN mkdir -p /app/marymount/edu/receiptscanner \
 && cp -r /app/src/marymount/edu/receiptscanner/* /app/marymount/edu/receiptscanner/

# Create runtime directories
RUN mkdir -p /app/uploads /app/logs

EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} marymount.edu.receiptscanner.web:app"]
