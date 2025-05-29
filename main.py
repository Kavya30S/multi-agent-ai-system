
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
import os
def main():
    classifier = ClassifierAgent()
    json_agent = JSONAgent()
    email_agent = EmailAgent()
         
    input_folder = "inputs"
    output_folder = "outputs"
    
    os.makedirs(output_folder, exist_ok=True)
         
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        try:
            with open(input_path, "r" if filename.endswith(".txt") or filename.endswith(".json") else "rb") as f:
                 input_data = f.read()
                 
                 result = classifier.process_input(input_data)
                 thread_id = result["thread_id"]
                 format_type = result["format"]
                 intent = result["intent"]
                 
                 output = {"thread_id": thread_id, "format": format_type, "intent": intent}
                 
                 if format_type == "JSON":
                     output.update(json_agent.process_json(thread_id, input_data))
                 elif format_type == "Email":
                     output.update(email_agent.process_email(thread_id, input_data))
                 elif format_type == "PDF":
                     output["message"] = "PDF processed, extracted text stored in memory"
                 
                 output_file = os.path.join(output_folder, f"output_{filename}.json")
                 with open(output_file, "w") as f:
                     import json
                     json.dump(output, f, indent=4)
                 
                 print(f"Processed {filename}: {output}")
        except Exception as e:
                 print(f"Error processing {filename}: {str(e)}")
if __name__ == "__main__":
     main()