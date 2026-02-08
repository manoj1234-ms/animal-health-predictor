import re
import pdfplumber
import io
from PIL import Image

def extract_text_from_file(uploaded_file):
    """Extracts raw text from PDF or Image."""
    text = ""
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        elif file_extension in ['png', 'jpg', 'jpeg']:
            # For images, we would ideally use OCR (pytesseract)
            # Since we want to keep it light, we'll mention it's for text-based PDFs
            # and just return a placeholder for images if tesseract isn't here
            text = "Image detected. Real-world implementation would use Tesseract/OCR."
            
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

def parse_animal_report(text):
    """
    Parses veterinary lab report text for key parameters using Regex.
    """
    data = {}
    text = text.lower()

    # Regex patterns for common lab values
    patterns = {
        'Animal': r'(species|animal|patient type):\s*(\w+)',
        'Age': r'age:\s*(\d+\.?\d*)',
        'WBC': r'wbc\D+(\d+\.?\d*)',
        'RBC': r'rbc\D+(\d+\.?\d*)',
        'Hemoglobin': r'(hg|hgb|hemoglobin)\D+(\d+\.?\d*)',
        'Platelets': r'(plt|platelets)\D+(\d+)',
        'Glucose': r'glucose\D+(\d+)',
        'ALT': r'alt\D+(\d+)',
        'AST': r'ast\D+(\d+)',
        'Urea': r'(urea|bun)\D+(\d+)',
        'Creatinine': r'(creat|creatinine)\D+(\d+\.?\d*)'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            val = match.group(2)
            if key == 'Animal':
                data[key] = val.capitalize()
            else:
                data[key] = float(val)

    # Symptom detection via keywords
    symptoms = {
        'Fever': ['fever', 'pyrexia', 'high temp'],
        'Lethargy': ['lethargy', 'tired', 'weakness'],
        'Vomiting': ['vomit', 'emesis'],
        'Diarrhea': ['diarrhea', 'loose stool'],
        'Coughing': ['cough', 'respiratory dist'],
        'Lameness': ['lameness', 'limp', 'gait']
    }
    
    found_symptoms = []
    for sym, keywords in symptoms.items():
        if any(kw in text for kw in keywords):
            found_symptoms.append(sym)
    
    data['Symptoms'] = found_symptoms
    
    return data
