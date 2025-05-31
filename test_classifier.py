from agents.classifier_agent import ClassifierAgent
import os

classifier = ClassifierAgent()
input_file = "inputs/sample_email.txt"

try:
    with open(input_file, "r") as f:
        input_data = f.read()
    result = classifier.process_input(input_data)
    print(f"Classifier Test Result: {result}")
except Exception as e:
    print(f"Classifier Test Failed: {str(e)}")