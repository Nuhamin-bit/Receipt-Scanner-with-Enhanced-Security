FROM python:3.12-slim

# install tesseract properly (this works in Docker)
RUN apt-get update && apt-get install -y tesseract-ocr

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.marymount.edu.receiptscanner.app:app", "--host", "0.0.0.0", "--port", "10000"]