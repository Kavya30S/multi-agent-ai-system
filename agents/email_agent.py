import re
import warnings
from transformers import pipeline
from agents.memory_manager import MemoryManager

# Suppress FutureWarning for clean_up_tokenization_spaces
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

class EmailAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.intents = ["Invoice", "RFQ", "Complaint", "Regulation"]

    def process_email(self, thread_id, email_content):
        """Extract sender, subject, urgency from email and classify intent using BERT."""
        sender = re.search(r"From: (.*?)\n", email_content)
        sender = sender.group(1) if sender else "Unknown"

        subject = re.search(r"Subject: (.*?)\n", email_content)
        subject = subject.group(1) if subject else "No Subject"

        urgency = "High" if "urgent" in email_content.lower() else "Normal"

        # Classify intent using BERT with refined heuristic
        content_lower = email_content.lower()
        result = self.classifier(email_content[:512])[0]
        label = result["label"]

        if "quote" in content_lower or "quotation" in content_lower:
            intent = "RFQ"
        elif "invoice" in content_lower or "amount" in content_lower:
            intent = "Invoice"
        elif label == "NEGATIVE":
            intent = "Complaint"
        else:
            intent = "Regulation"

        extracted_fields = {
            "sender": sender,
            "subject": subject,
            "urgency": urgency,
            "intent": intent
        }

        self.memory.save_context("Email", intent, extracted_fields)
        return {
            "thread_id": thread_id,
            "extracted_fields": extracted_fields
        }