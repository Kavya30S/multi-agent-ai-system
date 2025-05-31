from agents.email_agent import EmailAgent
import os

email_agent = EmailAgent()
input_file = "inputs/sample_email.txt"
thread_id = "test-thread-email"

try:
    with open(input_file, "r") as f:
        input_data = f.read()
    result = email_agent.process_email(thread_id, input_data)
    print(f"Email Agent Test Result: {result}")
except Exception as e:
    print(f"Email Agent Test Failed: {str(e)}")