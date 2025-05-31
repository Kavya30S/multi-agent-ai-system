import re
from agents.memory_manager import MemoryManager

class PDFAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.target_schema = {
            "invoice_number": str,
            "amount": float,
            "date": str,
            "sender": str
        }

    def process_pdf(self, thread_id, pdf_text):
        """Extract fields from PDF text, validate schema, and flag anomalies."""
        extracted_fields = {}
        anomalies = []

        # Define regex patterns for extraction
        patterns = {
            "invoice_number": r"Invoice #(\w+)",
            "amount": r"Amount: \$([\d,]+(?:\.\d{2})?)",
            "date": r"Date: (\d{4}-\d{2}-\d{2})",
            "sender": r"From: ([^\s]+@[^\s]+)"
        }

        # Extract fields using regex
        for key, pattern in patterns.items():
            match = re.search(pattern, pdf_text, re.IGNORECASE)
            if match:
                value = match.group(1)
                try:
                    # Convert to expected type
                    if key == "amount":
                        value = float(value.replace(",", ""))
                    if isinstance(value, self.target_schema[key]):
                        extracted_fields[key] = value
                    else:
                        anomalies.append(f"Invalid type for {key}: expected {self.target_schema[key]}, got {type(value)}")
                except ValueError:
                    anomalies.append(f"Invalid format for {key}: {value}")
            else:
                anomalies.append(f"Missing field: {key}")

        self.memory.save_context("PDF", "Processed", extracted_fields)
        return {
            "thread_id": thread_id,
            "extracted_fields": extracted_fields,
            "anomalies": anomalies
        }