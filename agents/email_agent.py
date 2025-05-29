import re
from transformers import pipeline
from agents.memory_manager import MemoryManager

class EmailAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    def process_email(self, thread_id, email_content):
        """Extract sender, intent, urgency from email and format for CRM."""
        sender = re.search(r"From: (.*?)\n", email_content)
        sender = sender.group(1) if sender else "Unknown"

        subject = re.search(r"Subject: (.*?)\n", email_content)
        subject = subject.group(1) if subject else "No Subject"

        urgency = "High" if "urgent" in email_content.lower() else "Normal"
        intent_result = self.nlp(email_content[:512])[0]
        intent = "Complaint" if intent_result["label"] == "NEGATIVE" else "RFQ"

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