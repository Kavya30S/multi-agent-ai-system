Multi-Agent AI System
A Python-based multi-agent system that processes PDF, JSON, and Email inputs, classifies their format and intent, and routes them to specialized agents. Shared context is maintained using SQLite. This project was developed as part of an internship screening assignment.

Features
Classifier Agent: Identifies input format (PDF, JSON, Email) and intent (Invoice, RFQ, Complaint, Regulation).
JSON Agent: Extracts and validates JSON fields against a target schema, flagging anomalies.
Email Agent: Extracts sender, subject, urgency, and intent from emails, formatting for CRM use.
Shared Memory: Uses SQLite to store context (source, intent, extracted fields) for traceability.
Handles unseen data robustly using regex and a pre-trained LLM (distilbert).

git clone https://github.com/Kavya30S/multi-agent-ai-system.git
cd multi-agent-ai-system

Create Conda Environment:
conda create -n multi_agent_system python=3.10
conda activate multi_agent_system

Install Dependencies:
pip install -r requirements.txt

Run the Application:
python main.py
Folder Structure
agents/: Contains agent scripts (classifier_agent.py, json_agent.py, email_agent.py, memory_manager.py).
inputs/: Sample input files (sample_email.txt, sample_rfq.json, sample_invoice.pdf, sample_complaint.txt, sample_invalid.json).
outputs/: Generated output JSON files.
memory/: SQLite database (memory.db).
LICENSE: MIT License for the project.
requirements.txt: Project dependencies.
README.md: This file.
Sample Inputs
sample_email.txt: An email requesting a quotation.
sample_rfq.json: A JSON file with invoice details.
sample_invoice.pdf: A PDF invoice.
sample_complaint.txt: An email with a complaint.
sample_invalid.json: A malformed JSON to test anomaly detection.

Expected Outputs
Output JSON files in outputs/ with format, intent, and extracted fields. Example for sample_email.txt:

json


{
    "thread_id": "uuid",
    "format": "Email",
    "intent": "RFQ",
    "extracted_fields": {
        "sender": "customer@example.com",
        "subject": "Request for Quotation",
        "urgency": "High",
        "intent": "RFQ"
    }
}
SQLite database (memory.db) stores context for traceability, viewable with DB Browser for SQLite.

Video Demo
Watch the demo (to be updated after hosting).

Future Improvements
Fine-tune the LLM for more accurate intent classification.
Add support for additional input formats (e.g., CSV).
Implement real-time processing via a web interface.