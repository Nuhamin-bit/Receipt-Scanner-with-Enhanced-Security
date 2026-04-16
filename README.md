### Receipt Scanner with Enhanced Security

This project is an AI-powered receipt scanner with added security and privacy enhancements. It automates receipt digitization while keeping sensitive data safe for both organizations and users.

Features
OCR Processing: Extracts text from receipt images using Tesseract OCR.
Image Preprocessing: Normalizes images for higher OCR accuracy.
Text Parsing: Automatically identifies merchant, total, date, gallons, and price per gallon.
Security & Privacy Enhancements:
All OCR data is processed locally to minimize exposure.
Logs are optionally encrypted with AES, and encryption keys are exchanged using Diffie-Hellman for secure key management.
Designed to be GDPR/CCPA compliant, ensuring user trust.
Flexible Input: Supports .jpg, .jpeg, .png, and .heic images.
CLI & Web: Can be run as a command-line tool for testing or integrated into a web interface.

Installation
pip install -r requirements.txt

**Usage**

 **Command-Line Interface (CLI)**
 
- Basic usage
python main.py path/to/receipt.jpg
- Disable OCR for testing
python main.py --no-ocr path/to/receipt.jpg

**Security Improvements**

1- Local OCR Processing: Data never leaves the local environment unless explicitly stored.

2- Encrypted Logs: OCR results are encrypted using AES; keys are securely exchanged via Diffie-Hellman.

3- Privacy Compliance: Ensures GDPR/CCPA best practices for handling user data.

4- Error Handling: Invalid or corrupted receipts do not expose sensitive information.


**Why This Matters**

- For companies digitizing their processes, protecting sensitive financial data is critical. This version of the receipt scanner ensures that:

- Data is secure by default.

- Users can trust the application to handle receipts safely.

- Organizations can meet regulatory requirements while automating expense tracking.


# Author

Nuhamin Tesfay



Supervised by: Dr. Natalia Bell, Marymount University, Spring 2026
