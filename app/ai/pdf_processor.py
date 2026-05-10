import os
import pdfplumber
import pytesseract
from PIL import Image
from flask import current_app

def extract_text_from_pdf(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    text = ""
    try:
        # Strategy 1: Standard text extraction
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Strategy 2: OCR if text is sparse (likely scanned PDF)
        # Note: Requires tesseract installed on the host/container
        if len(text.strip()) < 100:
            # Placeholder for OCR processing
            pass
            
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text
