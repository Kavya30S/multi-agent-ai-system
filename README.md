# Multi-Agent AI System (Streamlit)

This project is a Streamlit-based multi-agent AI system that processes uploaded files (`.txt`, `.json`, `.pdf`), classifies their format (`Email`, `JSON`, `PDF`) and intent (`Invoice`, `RFQ`, `Complaint`, `Regulation`), and extracts relevant fields. It uses a local BERT model (`distilbert-base-uncased-finetuned-sst-2-english`) with a keyword-based heuristic for intent classification, requiring no external API. Results are stored in a SQLite database (`memory/memory.db`) and as JSON files in `outputs/`. The app runs locally via Streamlit and is synced with GitHub.

**GitHub Repository**: github.com/Kavya30S/multi-agent-ai-system
**Live Video Demo Google Drive**:https://drive.google.com/file/d/1OT90A7PU24iwxtaD7q9ZY2XKLs4nRWER/view?usp=drivesdk

## **Table of Contents**

- Project Overview
- Folder Structure
- Expected Outputs
- Step-by-Step Working
- Troubleshooting

## **Project Overview**

The system handles different file types, identifies their format and purpose, and pulls out key information using specialized agents.

### *Key Features*

- **Text Files (**`.txt`**)**: Treated as emails, extracting `sender`, `subject`, `urgency`, and intent.
- **JSON Files (**`.json`**)**: Extracts fields like `invoice_number`, `amount`, `date`, `sender`.
- **PDF Files (**`.pdf`**)**: Extracts fields using text extraction.
- **Intent Classification**: Uses a local BERT model with keywords (e.g., “quote” for `RFQ`).
- **Storage**: Saves results in `memory/memory.db` and `outputs/`.
- **Interface**: Streamlit app at `http://localhost:8501`.

## **Folder Structure**

The project is organized as follows.

### *Directory Details*

```
multi-agent-ai-system/
├── agents/
│   ├── __init__.py           # Makes agents a package
│   ├── classifier_agent.py   # Classifies format and intent
│   ├── email_agent.py        # Processes emails
│   ├── json_agent.py         # Processes JSON files
│   ├── memory_manager.py     # Manages SQLite database
│   ├── pdf_agent.py          # Processes PDFs
├── inputs/
│   ├── sample_email.txt      # Sample email (RFQ)
│   ├── sample_rfq.json       # Sample JSON (Invoice)
│   ├── sample_invoice.pdf    # Sample PDF (Invoice)
├── outputs/                  # Stores JSON output files
├── memory/
│   └── memory.db             # SQLite database
├── .gitignore                # Excludes memory.db, outputs/, etc.
├── app.py                    # Streamlit app
├── requirements.txt          # Dependencies
├── test_classifier.py        # Tests ClassifierAgent
├── test_email_agent.py       # Tests EmailAgent
├── test_json_agent.py        # Tests JSONAgent
├── test_pdf_agent.py         # Tests PDFAgent
├── README.md                 # Project documentation
├── demo/                     # (Optional) Demo video
│   └── demo.mp4
```

## **Expected Outputs**

Results for sample files when processed via Streamlit or test scripts.

### *sample_email.txt*

**Content**:

```
From: customer@example.com
Subject: Request for Quotation
Hi, please provide a quote for 100 units of Product X. This is urgent.
```

**Output**:

```
File: sample_email.txt
Format: Email
Intent: RFQ
Extracted Fields: {"sender": "customer@example.com", "subject": "Request for Quotation", "urgency": "High", "intent": "RFQ"}
Output saved to: outputs/output_sample_email.txt.json
```

### *sample_rfq.json*

**Content**:

```
{
    "invoice_number": "INV123",
    "amount": 5000.0,
    "date": "2025-05-31",
    "sender": "vendor@example.com"
}
```

**Output**:

```
File: sample_rfq.json
Format: JSON
Intent: Invoice
Extracted Fields: {"invoice_number": "INV123", "amount": 5000.0, "date": "2025-05-31", "sender": "vendor@example.com"}
Output saved to: outputs/output_sample_rfq.json
```

### *sample_invoice.pdf*

**Content**:

```
Invoice #INV456
Amount: $10,000
Date: 2025-05-31
From: supplier@example.com
```

**Output**:

```
File: sample_invoice.pdf
Format: PDF
Intent: Invoice
Extracted Fields: {"invoice_number": "INV456", "amount": 10000.0, "date": "2025-05-31", "sender": "supplier@example.com"}
Output saved to: outputs/output_sample_invoice.pdf.json
```

## **Step-by-Step Working**

Steps to set up and run the project.

### *Prerequisites*

- Anaconda at `C:\Users\THINKPAD\anaconda3`.
- VS Code with Python extension.
- Git for version control.
- Python 3.10 in `multi_agent_system` Conda environment.

### *Step 1: Clone the Repository*

1. Open Anaconda Prompt.

2. Navigate to:

   ```
   cd C:\Users\THINKPAD\Documents
   ```

3. Clone:

   ```
   git clone https://github.com/Kavya30S/multi-agent-ai-system.git
   ```

4. Enter directory:

   ```
   cd multi-agent-ai-system
   ```

### *Step 2: Set Up Conda Environment*

1. Activate environment:

   ```
   conda activate multi_agent_system
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

### *Step 3: Verify Input Files*

Ensure `inputs/` contains:

- `sample_email.txt`
- `sample_rfq.json`
- `sample_invoice.pdf`

### *Step 4: Run Test Scripts*

1. ClassifierAgent:

   ```
   python test_classifier.py
   ```

2. EmailAgent:

   ```
   python test_email_agent.py
   ```

3. JSONAgent:

   ```
   python test_json_agent.py
   ```

4. PDFAgent:

   ```
   python test_pdf_agent.py
   ```

### *Step 5: Run Streamlit App*

1. Launch:

   ```
   streamlit run app.py
   ```

2. Open `http://localhost:8501`.

3. Upload sample files and check results.

### *Step 6: Verify Outputs*

1. Check `outputs/`:

   ```
   dir outputs
   ```

2. Inspect `memory/memory.db` with DB Browser for SQLite.

### *Step 7: Record Demo (Optional)*

1. Use OBS Studio to record VS Code, Anaconda Prompt, browser, and File Explorer.

2. Save and push:

   ```
   mkdir demo
   move path_to_recording.mp4 demo/demo.mp4
   git add demo/demo.mp4
   git commit -m "Added demo video"
   git push origin main
   ```

### *Step 8: Push to GitHub*

1. Commit changes:

   ```
   git add .
   git commit -m "Updated README formatting"
   git push origin main
   ```

## **Troubleshooting**

Solutions for common issues.

### *Dependency Issues*

- Check:

  ```
  pip show streamlit pdfplumber transformers torch
  ```

- Reinstall:

  ```
  pip install -r requirements.txt
  ```

### *PDF Processing Errors*

- Verify `pdfplumber`.
- Ensure `sample_invoice.pdf` has text.

### *Intent Misclassification*

- Check `sample_email.txt` for “quote”.
- Update heuristics in `classifier_agent.py` or `email_agent.py`.

### *Database Issues*

- Check `memory/` permissions.
- Delete `memory.db` to recreate.

### *Streamlit Issues*

- Ensure port 8501 is free:

<<<<<<< HEAD
  # 
=======
  # 
>>>>>>> cc67894aad38c7eec6b88e04cb5bd5ad30f20d7c
