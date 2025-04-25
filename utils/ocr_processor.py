import re
import pytesseract
from PIL import Image

def extract_text(image):
    custom_config = r'--oem 3 --psm 6'
    try:
        text = pytesseract.image_to_string(image, config=custom_config)
        return text
    except pytesseract.TesseractError as e:
        print(f"OCR Error: {str(e)}")
        return ""

def parse_loan_data(text):
    patterns = {
        'name': r'(?:Name|Full Name)[:\s]+((?:(?!Address)[A-Za-z .-])+)',
        'address': r'(?:Address|Residence)[:\s]+(.*?)(?=\n\s*(?:Annual Income|Income|$))',
        'income': r'(?:Annual Income|Income)[:\s\$]+([\d,]+)',
        'loan_amount': r'(?:Loan Amount|Amount Requested)[:\s\$]+([\d,]+)',
        'ssn': r'\b(\d{3}-\d{2}-\d{4})\b'
    }
    
    results = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        results[field] = match.group(1).strip() if match else ''
    
    return results