from fastapi import FastAPI, UploadFile, File
import tempfile

from .processor import ReceiptScanner

app = FastAPI()
scanner = ReceiptScanner()


@app.get("/")
def home():
    return {"message": "Receipt Scanner API running 🚀"}


@app.post("/upload-receipt")
async def upload_receipt(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = scanner.parse_image(tmp_path)

    return {
        "status": "success",
        "result": result
    }