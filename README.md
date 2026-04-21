### Receipt Scanner — Secure Financial Intelligence System

### Overview

The Receipt Scanner System is a secure, cloud-ready financial data processing platform that converts receipt images into structured, analyzable financial records.

It integrates:

  - OCR (Tesseract)
  - FastAPI backend
  - AES-256 encryption
  - Diffie-Hellman key exchange
  - SQLite database
  - Financial analytics engine
  - Cloud deployment readiness (Render)

    
### Problem Statement

Manual receipt tracking is:

    - Slow
    - Error-prone
    - Unstructured
    - Not secure

This system automates financial data extraction and introduces security + analytics.

### System Architecture

  User Upload
  
            ↓   
       
  FastAPI Endpoint
  
            ↓
       
  Image Preprocessing
  
           ↓
       
  OCR (Tesseract)
  
           ↓
       
  Text Parsing (Regex + Rules)
  
          ↓
       
  AES Encryption Layer
  
           ↓
       
  SQLite Database
  
          ↓
       
  Analytics Engine


### Security Features

- AES-256 encryption for financial data
- Diffie-Hellman key exchange for secure key generation
- Secure structured logging
- Protected database storage

### API Endpoints

Method	Endpoint	Description: 

- POST	/upload-receipt	Upload receipt image
- GET	/analytics/monthly	Monthly spending summary
- GET	/analytics/merchant-summary	Spending by merchant
- GET	/export/csv	Export financial data

### Deployment

- Backend: FastAPI
- Hosting: Render
- Database: SQLite
- Ready for Docker containerization

## Digital Transformation Impact

- Converts manual receipts → automated financial system
- Adds enterprise-grade security
- Enables cloud accessibility
- Provides structured financial analytics

### Future Improvements

- Machine learning receipt parsing
- React dashboard UI
- Multi-user authentication system
- Cloud database migration 


## Author
Nuhamin Tesfay

