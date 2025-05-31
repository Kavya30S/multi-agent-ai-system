Multi-Agent AI System (Streamlit)

This project is a Streamlit-based multi-agent AI system designed to process uploaded files (.txt, .json, .pdf), classify their format (Email, JSON, PDF) and intent (Invoice, RFQ, Complaint, Regulation), and extract relevant fields. It uses a local BERT model (distilbert-base-uncased-finetuned-sst-2-english) with a keyword-based heuristic for intent classification, ensuring no external API dependency. The system employs a modular agent architecture, stores results in a SQLite database (memory/memory.db), and saves outputs as JSON files in outputs/. The application is hosted locally via Streamlit and synced with GitHub for version control.
GitHub Repository: github.com/Kavya30S/multi-agent-ai-system
Project Overview

Text Files (.txt): Treated as emails, extracting sender, subject, urgency, and intent using BERT and regex.
JSON Files (.json): Validates and extracts fields like invoice_number, amount, date, sender.
PDF Files (.pdf): Extracts fields using regex after text extraction with pdfplumber.
Intent Classification: Uses a local BERT model with a heuristic prioritizing keywords (e.g., “quote” for RFQ, “invoice” for Invoice).
Storage: Results are stored in memory/memory.db (SQLite) and outputs/ (JSON).
Interface: Streamlit app at http://localhost:8501 for file uploads and result display.

Folder Structure
multi-agent-ai-system/
├── agents/
│   ├── __init__.py               # Empty file to make agents a package
│   ├── classifier_agent.py       # Classifies format and intent using BERT
│   ├── email_agent.py            # Processes emails, extracts fields
│   ├── json_agent.py             # Processes JSON files, validates fields
│   ├── memory_manager.py         # Manages SQLite database storage
│   ├── pdf_agent.py              # Processes PDFs, extracts fields
├── inputs/
│   ├── sample_email.txt          # Sample email for testing (RFQ)
│   ├── sample_rfq.json           # Sample JSON for testing (Invoice)
│   ├── sample_invoice.pdf        # Sample PDF for testing (Invoice)
├── outputs/                      # Directory for JSON output files
├── memory/
│   └── memory.db                 # SQLite database for storing results
├── .gitignore                    # Excludes .env, memory.db, outputs/, etc.
├── app.py                        # Streamlit app for file upload and processing
├── requirements.txt              # Python dependencies
├── test_classifier.py            # Test script for ClassifierAgent
├── test_email_agent.py           # Test script for EmailAgent
├── test_json_agent.py            # Test script for JSONAgent
├── test_pdf_agent.py             # Test script for PDFAgent
├── README.md                     # Project documentation
├── demo/                         # (Optional) Directory for demo video
│   └── demo.mp4                  # Demo video of project

##Expected Outputs
Below are the expected results when processing the sample files via the Streamlit app or test scripts.
sample_email.txt
Content:
From: customer@example.com
Subject: Request for Quotation
Hi, please provide a quote for 100 units of Product X. This is urgent.

*Output:
File: sample_email.txt
Format: Email
Intent: RFQ
Extracted Fields: {"sender": "customer@example.com", "subject": "Request for Quotation", "urgency": "High", "intent": "RFQ"}
Output saved to: outputs/output_sample_email.txt.json

sample_rfq.json
Content:
{
    "invoice_number": "INV123",
    "amount": 5000.0,
    "date": "2025-05-29",
    "sender": "vendor@example.com"
}

*Output:
File: sample_rfq.json
Format: JSON
Intent: Invoice
Extracted Fields: {"invoice_number": "INV123", "amount": 5000.0, "date": "2025-05-29", "sender": "vendor@example.com"}
Output saved to: outputs/output_sample_rfq.json

sample_invoice.pdf
Content:
Invoice #INV456
Amount: $10,000
Date: 2025-05-29
From: supplier@example.com

*Output:
File: sample_invoice.pdf
Format: PDF
Intent: Invoice
Extracted Fields: {"invoice_number": "INV456", "amount": 10000.0, "date": "2025-05-29", "sender": "supplier@example.com"}
Output saved to: outputs/output_sample_invoice.pdf.json

##Step-by-Step Working
Follow these steps to set up and run the project on your local machine.
Prerequisites

Anaconda: Installed at C:\Users\THINKPAD\anaconda3.
VS Code: With Python extension for editing and debugging.
Git: For cloning and version control.
Python 3.10: Included in the multi_agent_system Conda environment.
Hardware: Windows PC (e.g., ThinkPAD) with sufficient memory for BERT model inference.

Step 1: Clone the Repository

Open Anaconda Prompt.
Navigate to your documents directory:cd C:\Users\THINKPAD\Documents


Clone the repository:git clone https://github.com/Kavya30S/multi-agent-ai-system.git


Enter the project directory:cd multi-agent-ai-system

Expected Output: Repository is cloned, and you’re in the project folder.

Step 2: Set Up Conda Environment

Activate the Conda environment:conda activate multi_agent_system

Expected Output: Prompt shows (multi_agent_system).
Install dependencies:pip install -r requirements.txt

Expected Output:Successfully installed streamlit-1.31.0 pdfplumber-0.11.4 transformers-4.44.2 torch-2.4.1



Step 3: Verify Input Files
Ensure the inputs/ directory contains:

sample_email.txt:From: customer@example.com
Subject: Request for Quotation
Hi, please provide a quote for 100 units of Product X. This is urgent.


sample_rfq.json:{
    "invoice_number": "INV123",
    "amount": 5000.0,
    "date": "2025-05-29",
    "sender": "vendor@example.com"
}


sample_invoice.pdf with text:Invoice #INV456
Amount: $10,000
Date: 2025-05-29
From: supplier@example.com



Expected Output: Files are present in inputs/. Create sample_invoice.pdf manually (e.g., using a text editor and saving as PDF) if missing.
Step 4: Run Test Scripts
Test each agent to verify functionality:

Test ClassifierAgent:python test_classifier.py

Expected Output:Classifier Test Result: {'thread_id': '<uuid>', 'format': 'Email', 'intent': 'RFQ', 'text_content': 'From: customer@example.com\nSubject: Request for Quotation\nHi, please provide a quote for 100 units of Product X. This is urgent.'}


Test EmailAgent:python test_email_agent.py

Expected Output:Email Agent Test Result: {'thread_id': 'test-thread-email', 'extracted_fields': {'sender': 'customer@example.com', 'subject': 'Request for Quotation', 'urgency': 'High', 'intent': 'RFQ'}}


Test JSONAgent:python test_json_agent.py

Expected Output:JSON Agent Test Result: {'thread_id': 'test-thread-json', 'extracted_fields': {'invoice_number': 'INV123', 'amount': 5000.0, 'date': '2025-05-29', 'sender': 'vendor@example.com'}, 'anomalies': []}


Test PDFAgent:python test_pdf_agent.py

Expected Output:PDF Agent Test Result: {'thread_id': 'test-thread-pdf', 'extracted_fields': {'invoice_number': 'INV456', 'amount': 10000.0, 'date': '2025-05-29', 'sender': 'supplier@example.com'}, 'anomalies': []}



Step 5: Run Streamlit App

Launch the Streamlit app:streamlit run app.py

Expected Output: Browser opens at http://localhost:8501.
Upload sample files:
Navigate to http://localhost:8501.
Use the file uploader to select sample_email.txt, sample_rfq.json, and sample_invoice.pdf.


Verify results:
Results are displayed on the webpage (see Expected Outputs above).
JSON files are saved in outputs/ (e.g., output_sample_email.txt.json).
Database entries are added to memory/memory.db.



Step 6: Verify Outputs

Check outputs/ for JSON files:dir outputs

Expected Output: Files like output_sample_email.txt.json, output_sample_rfq.json, output_sample_invoice.pdf.json.
Inspect memory/memory.db using DB Browser for SQLite:
Open memory/memory.db.
Check the context table for entries with format, intent, and context_data.Expected Output: Entries for each processed file with corresponding fields.



Step 7: Record Demo (Optional)

Use OBS Studio to record:
VS Code showing project files.
Anaconda Prompt running test scripts.
Browser at http://localhost:8501 with file uploads and results.
File Explorer showing outputs/ and memory/memory.db.


Save the video:mkdir demo
move path_to_recording.mp4 demo/demo.mp4


Push to GitHub:git add demo/demo.mp4
git commit -m "Added demo video"
git push origin main

Expected Output: Video is uploaded to https://github.com/Kavya30S/multi-agent-ai-system.

Step 8: Push to GitHub

Commit any changes:git add .
git commit -m "Updated project with refined intent classification and README"
git push origin main

Expected Output: Changes are pushed to the repository.

Troubleshooting

Dependency Issues:
Verify installed packages:pip show streamlit pdfplumber transformers torch


Reinstall if needed:pip install -r requirements.txt




PDF Processing Errors:
Ensure pdfplumber is installed.
Verify sample_invoice.pdf contains text (not an image-based PDF).


Intent Misclassification:
Check sample_email.txt for keywords like “quote” or “quotation”.
Update classifier_agent.py or email_agent.py heuristics if needed.


Database Issues:
Ensure memory/ has write permissions:dir memory


Delete memory.db and rerun tests/app to recreate.


Streamlit Issues:
Verify port 8501 is free:netstat -a -n | find "8501"


Restart the app if needed.



Notes

The BERT model (distilbert-base-uncased-finetuned-sst-2-english) uses sentiment analysis with a heuristic for intent classification. For higher accuracy, fine-tuning on a custom dataset would be ideal but is beyond the current scope.
The project is designed to run offline, requiring no API keys, making it suitable for local deployment.

