import pdfplumber
import json
import re
from transformers import pipeline
from agents.memory_manager import MemoryManager

class ClassifierAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.intents = ["Invoice", "RFQ", "Complaint", "Regulation"]

    def classify_format(self, input_data):
        """Classify input format as PDF, JSON, or Email."""
        if isinstance(input_data, str):
            try:
                json.loads(input_data)
                return "JSON"
            except ValueError:
                if re.match(r".*From:.*Subject:.*", input_data, re.DOTALL):
                    return "Email"
        elif isinstance(input_data, bytes) or hasattr(input_data, "read"):
            return "PDF"
        return "Unknown"

    def classify_intent(self, text):
        """Classify intent using LLM."""
        result = self.nlp(text[:512])[0]  # Limit to 512 tokens
        # Map sentiment to intents (simplified for demo; fine-tune for real use)
        intent_map = {"POSITIVE": "RFQ", "NEGATIVE": "Complaint"}
        intent = intent_map.get(result["label"], "Invoice")
        return intent

    def process_input(self, input_data):
        """Process input, classify, and route to appropriate agent."""
        format_type = self.classify_format(input_data)
        text_content = ""

        if format_type == "PDF":
            with pdfplumber.open(input_data) as pdf:
                text_content = "".join(page.extract_text() or "" for page in pdf.pages)
        elif format_type == "JSON":
            text_content = json.dumps(json.loads(input_data))
        elif format_type == "Email":
            text_content = input_data
        else:
            raise ValueError("Unsupported format")

        intent = self.classify_intent(text_content)
        thread_id = self.memory.save_context(format_type, intent, {"raw_text": text_content})

        return {
            "thread_id": thread_id,
            "format": format_type,
            "intent": intent,
            "text_content": text_content
        }