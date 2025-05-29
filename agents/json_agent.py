import json
from agents.memory_manager import MemoryManager

class JSONAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.target_schema = {
            "invoice_number": str,
            "amount": float,
            "date": str,
            "sender": str
        }

    def process_json(self, thread_id, json_data):
        """Process JSON input, validate schema, and flag anomalies."""
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            extracted_fields = {}
            anomalies = []

            for key, expected_type in self.target_schema.items():
                if key in data:
                    if isinstance(data[key], expected_type):
                        extracted_fields[key] = data[key]
                    else:
                        anomalies.append(f"Invalid type for {key}: expected {expected_type}, got {type(data[key])}")
                else:
                    anomalies.append(f"Missing field: {key}")

            self.memory.save_context("JSON", "Processed", extracted_fields)
            return {
                "thread_id": thread_id,
                "extracted_fields": extracted_fields,
                "anomalies": anomalies
            }
        except json.JSONDecodeError:
            return {"thread_id": thread_id, "error": "Invalid JSON"}