# Automated Loan Document Processor

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app/)

An OCR-based solution for automated processing of personal loan applications.

## Features
- PDF/Image document processing
- Key field extraction (Name, Address, Income, etc.)
- Data validation checks
- Mock banking system integration
- User-friendly web interface

![ss1](../loan-ocr-project/UI/ss1.png)
![ss2](../loan-ocr-project/UI/ss2.png)
![ss3](../loan-ocr-project/UI/ss3.png)

## Installation
1. Clone repository: (NOT NOW. ONLY AFTER TCS APPROVAL TO DISPLAY PROJECT)
```bash
git clone https://github.com/yourusername/loan-ocr-project.git


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Poppler (Windows): https://github.com/oschwartz10612/poppler-windows

## Usage
```bash
streamlit run main.py
```

## Configuration
Set paths in `main.py`:
```python
POPPLER_PATH = r"C:\poppler\bin"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Project Structure

### Folder Structure with Files
```
loan-ocr-project/
├── main.py
├── README.md
├── requirements.txt
├── samples/
│   ├── loan_app_1.pdf
│   └── loan_app_2.jpg
└── utils/
    ├── preprocessing.py
    ├── ocr_processor.py
    ├── validation.py
    └── integration.py
```


### `requirements.txt`
```text
streamlit==1.35.0
pytesseract==0.3.10
pillow==10.3.0
opencv-python-headless==4.9.0.80
python-magic==0.4.27
pdf2image==1.17.0
pymupdf==1.24.4
pandas==2.2.2
numpy==1.26.4
requests==2.31.0
python-dotenv==1.0.1
```

---

### Final Compliance Report

**Fully Implemented Features (17/20):**
1. Document preprocessing pipeline
2. OCR text extraction
3. Key field identification
4. Data validation system
5. Streamlit UI with manual correction
6. Mock banking integration
7. Error handling
8. Multi-format support (PDF/Images)
9. Temporary file management

**Recommendations:**
1. Add document classification for different doc types
2. Implement rate limiting for API calls
3. Add audit logging for compliance
4. Create test dataset with 50+ sample documents
