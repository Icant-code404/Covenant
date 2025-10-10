# test_pdf.py
from utils.pdf_parser import extract_text_from_pdf

file_path = "C:/Users/Samuel/Desktop/Masters/gre-sample-questions.pdf"
text = extract_text_from_pdf(file_path)
print(text[:500])  # print first 500 chars for testing
