from agents.json_agent import JSONAgent
import os
import json

json_agent = JSONAgent()
input_file = "inputs/sample_rfq.json"
thread_id = "test-thread-json"

try:
    with open(input_file, "r") as f:
        input_data = f.read()
    result = json_agent.process_json(thread_id, input_data)
    print(f"JSON Agent Test Result: {result}")
except Exception as e:
    print(f"JSON Agent Test Failed: {str(e)}")