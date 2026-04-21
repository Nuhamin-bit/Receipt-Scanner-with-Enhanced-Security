from fastapi import FastAPI, UploadFile, File
import tempfile

from .processor import ReceiptScanner, ImagePreprocessor, OCRProcessor, TextProcessor
from .database import SessionLocal, Receipt


app = FastAPI()

# ---------------------------
# OCR Pipeline
# ---------------------------
scanner = ReceiptScanner(
    use_ocr=True,
    image_processor=ImagePreprocessor(),
    ocr_processor=OCRProcessor(),
    text_processor=TextProcessor(),
)

# ---------------------------
# Save receipt to DB
# ---------------------------
def save_receipt(data):
    db = SessionLocal()

    receipt = Receipt(
        merchant=data.get("merchant", "unknown"),
        date=data.get("date", "unknown"),
        total=data.get("total", 0.0),
        tax=data.get("tax", 0.0),
        items=data.get("items", []),
    )

    db.add(receipt)
    db.commit()
    db.close()

# ---------------------------
# Health check
# ---------------------------
@app.get("/")
def home():
    return {"message": "Receipt Scanner API running"}

# ---------------------------
# Upload + OCR + Save
# ---------------------------
@app.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    raw_text = scanner.parse_image(tmp_path)
    raw_text = raw_text[:3000]  # 👈 ADD IT HERE

    structured = {
        "merchant": extract_merchant(raw_text),
        "total": extract_total(raw_text),
        "category": categorize(raw_text),
        "raw_text": raw_text
    }

    save_receipt(structured)

    return {
        "status": "saved",
        "data": structured
    }
# ---------------------------
# Analytics: Monthly Spending
# ---------------------------
@app.get("/analytics/monthly")
def monthly_spending():
    db = SessionLocal()

    receipts = db.query(Receipt).all()
    total_spent = sum(r.total for r in receipts)

    db.close()

    return {
        "total_spent": total_spent,
        "number_of_receipts": len(receipts)
    }

# ---------------------------
# Analytics: Merchant Summary
# ---------------------------
@app.get("/analytics/merchant-summary")
def merchant_summary():
    db = SessionLocal()

    receipts = db.query(Receipt).all()

    summary = {}

    for r in receipts:
        merchant = r.merchant or "unknown"
        summary[merchant] = summary.get(merchant, 0) + r.total

    db.close()

    return summary

# ---------------------------
# Export to CSV
# ---------------------------
@app.get("/export/csv")
def export_csv():
    import pandas as pd
    db = SessionLocal()

    receipts = db.query(Receipt).all()

    data = [
        {
            "merchant": r.merchant,
            "date": r.date,
            "total": r.total,
            "tax": r.tax
        }
        for r in receipts
    ]

    db.close()

    df = pd.DataFrame(data)
    file_path = "receipts_export.csv"
    df.to_csv(file_path, index=False)

    return {
        "status": "exported",
        "file": file_path,
        "rows": len(data)
    }