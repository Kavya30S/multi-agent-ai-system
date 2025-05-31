import streamlit as st
import os
import json
import pdfplumber
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from agents.pdf_agent import PDFAgent

# Initialize agents
classifier = ClassifierAgent()
json_agent = JSONAgent()
email_agent = EmailAgent()
pdf_agent = PDFAgent()

# Set up output folder
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

st.title("Multi-Agent AI System")
st.write("Upload a file (.txt, .json, .pdf) to classify its format and intent, and extract relevant fields.")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["txt", "json", "pdf"])

if uploaded_file is not None:
    # Read file content
    try:
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                input_data = "".join(page.extract_text() or "" for page in pdf.pages)
            format_type = "PDF"
        else:
            input_data = uploaded_file.read().decode("utf-8")
            format_type = classifier.classify_format(input_data)

        # Process with ClassifierAgent
        result = classifier.process_input(input_data)
        thread_id = result["thread_id"]
        intent = result["intent"]
        text_content = result["text_content"]

        # Route to appropriate agent
        output = {"thread_id": thread_id, "format": format_type, "intent": intent}

        if format_type == "JSON":
            output.update(json_agent.process_json(thread_id, input_data))
        elif format_type == "Email":
            output.update(email_agent.process_email(thread_id, input_data))
        elif format_type == "PDF":
            output.update(pdf_agent.process_pdf(thread_id, input_data))

        # Save output to file
        output_file = os.path.join(output_folder, f"output_{uploaded_file.name}.json")
        with open(output_file, "w") as f:
            json.dump(output, f, indent=4)

        # Display results
        st.subheader("Results")
        st.write(f"**File**: {uploaded_file.name}")
        st.write(f"**Format**: {format_type}")
        st.write(f"**Intent**: {intent}")
        if format_type in ["JSON", "Email", "PDF"]:
            st.write("**Extracted Fields**:")
            st.json(output["extracted_fields"])
        if "anomalies" in output and output["anomalies"]:
            st.write("**Anomalies**:")
            for anomaly in output["anomalies"]:
                st.write(f"- {anomaly}")
        st.write(f"**Output saved to**: {output_file}")

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

# Option to clear memory
if st.button("Clear Memory"):
    memory_db = "memory/memory.db"
    if os.path.exists(memory_db):
        os.remove(memory_db)
        st.success("Memory database cleared!")
    else:
        st.warning("No memory database found.")