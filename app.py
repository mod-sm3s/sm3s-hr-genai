import os
import re
import csv
import shutil
import tempfile
import streamlit as st
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# Extract text from PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Extract name (from filename), email, and phone number
def extract_info(text, file_name):
    name = os.path.splitext(file_name)[0].replace("_", " ").title()
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text)

    email = email_match.group(0) if email_match else "Not found"
    phone = phone_match.group(0) if phone_match else "Not found"
    return name, email, phone

# Get score from Gemini based on resume vs job description
def get_resume_score(jd_text, resume_text):
    prompt = (
        f"Evaluate the candidate's resume against the job description below.\n\n"
        f"Job Description:\n{jd_text}\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Give a score out of 100 for how well this candidate fits the job. Just return the score number only."
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        score = int(re.search(r'\d+', response.content).group())
        return min(score, 100)
    except:
        return 0

# Streamlit App
st.title("Resume Evaluator 📄✨")

# File uploads
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_files = st.file_uploader("Upload Resumes (multiple PDFs)", type=["pdf"], accept_multiple_files=True)

if jd_file and resume_files:
    if st.button("Evaluate Resumes"):
        with st.spinner("Processing..."):

            jd_text = extract_text_from_pdf(jd_file)
            results = []

            for resume in resume_files:
                resume_text = extract_text_from_pdf(resume)
                name, email, phone = extract_info(resume_text, resume.name)
                score = get_resume_score(jd_text, resume_text)
                results.append([name, email, phone, score])

            # Sort by score descending
            results.sort(key=lambda x: x[3], reverse=True)

            # Save to CSV
            csv_path = os.path.join(tempfile.gettempdir(), "resume_scores.csv")
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Email", "Mobile", "Score"])
                writer.writerows(results)

            st.success("Evaluation complete!")
            st.download_button("Download CSV", data=open(csv_path, "rb"), file_name="resume_scores.csv", mime="text/csv")
