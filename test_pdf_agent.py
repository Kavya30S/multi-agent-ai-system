from agents.pdf_agent import PDFAgent
import pdfplumber
import os

pdf_agent = PDFAgent()
input_file = "inputs/sample_invoice.pdf"
thread_id = "test-thread-pdf"

try:
    with pdfplumber.open(input_file) as pdf:
        input_data = "".join(page.extract_text() or "" for page in pdf.pages)
    result = pdf_agent.process_pdf(thread_id, input_data)
    print(f"PDF Agent Test Result: {result}")
except Exception as e:
    print(f"PDF Agent Test Failed: {str(e)}")