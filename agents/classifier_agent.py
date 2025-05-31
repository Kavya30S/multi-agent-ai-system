import json
import uuid
import warnings
from transformers import pipeline
from agents.memory_manager import MemoryManager

# Suppress FutureWarning for clean_up_tokenization_spaces
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

class ClassifierAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.intents = ["Invoice", "RFQ", "Complaint", "Regulation"]

    def classify_format(self, content):
        """Classify the format of the input content."""
        try:
            json.loads(content)
            return "JSON"
        except ValueError:
            if "From:" in content and "Subject:" in content:
                return "Email"
        return "Unknown"

    def classify_intent(self, content):
        """Classify the intent using BERT with refined heuristic."""
        content_lower = content.lower()
        result = self.classifier(content[:512])[0]  # Limit to 512 tokens
        label = result["label"]

        # Refined heuristic
        if "quote" in content_lower or "quotation" in content_lower:
            return "RFQ"
        elif "invoice" in content_lower or "amount" in content_lower:
            return "Invoice"
        elif label == "NEGATIVE":
            return "Complaint"
        return "Regulation"

    def process_input(self, content):
        """Process input to classify format and intent."""
        thread_id = str(uuid.uuid4())
        format_type = self.classify_format(content)
        intent = self.classify_intent(content)

        self.memory.save_context(format_type, intent, {"content": content[:1000]})
        return {
            "thread_id": thread_id,
            "format": format_type,
            "intent": intent,
            "text_content": content
        }