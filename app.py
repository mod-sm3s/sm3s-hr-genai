import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import PyPDF2
from fpdf import FPDF

# Set API Key
google_api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", convert_system_message_to_human=True, google_api_key=google_api_key)

# Streamlit UI Setup

st.set_page_config(page_title="HR AI System", layout="wide", initial_sidebar_state="expanded")
st.title("HR GENAI APP")
st.image("logo.png", width=150)

# ---- STYLES ----
st.markdown("""
    <style>
        body {background-color: #0d1117; color: #e6edf3;}
        .stTextInput, .stTextArea, .stSelectbox, .stFileUploader {border: 2px solid #3ddc97;}
        .stButton>button {background: linear-gradient(90deg, #3ddc97, #00aaff); color: white;}
    </style>
""", unsafe_allow_html=True)

# ---- FUNCTION: Job Description Generator ----
def generate_job_description(title, industry=None, responsibilities=None, skills=None, experience=None):
    prompt = f"Generate a job description for a '{title}' role."
    
    if industry:
        prompt += f" Industry: {industry}."
    if responsibilities:
        prompt += f" Key Responsibilities: {responsibilities}."
    if skills:
        prompt += f" Required Skills: {skills}."
    if experience:
        prompt += f" Years of Experience: {experience}."

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# ---- FUNCTION: Resume Evaluator ----
def evaluate_resume(job_desc_text, resume_text):
    prompt = f"Evaluate the resume against the job description.\n\nJob Description:\n{job_desc_text}\n\nResume:\n{resume_text}\n\nHow well does this candidate fit?"
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# ---- FUNCTION: Extract Text from PDF ----
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# ---- STREAMLIT UI ----
tab1, tab2 = st.tabs(["📄 Job Description Generator", "📑 Resume Evaluator"])

# ---- TAB 1: Job Description Generator ----
with tab1:
    st.subheader("📄 Generate Job Description")
    
    title = st.text_input("Job Title (Required)", placeholder="e.g., Bank Teller")
    industry = st.text_input("Industry", placeholder="e.g., Banking, Finance")
    responsibilities = st.text_area("Key Responsibilities", placeholder="List key tasks")
    skills = st.text_area("Required Skills", placeholder="List skills needed")
    experience = st.number_input("Years of Experience", min_value=0, step=1)

    if st.button("Generate Description"):
        if title:
            job_desc = generate_job_description(title, industry, responsibilities, skills, experience)
            st.success("✅ Job Description Generated:")
            st.write(job_desc)

            # Save as PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(190, 10, job_desc)
            pdf_file = "job_description.pdf"
            pdf.output(pdf_file)
            st.download_button("Download PDF", data=open(pdf_file, "rb"), file_name=pdf_file, mime="application/pdf")

        else:
            st.error("⚠️ Please enter a Job Title.")

# ---- TAB 2: Resume Evaluator ----
with tab2:
    st.subheader("📑 Resume Evaluator")

    job_desc_file = st.file_uploader("Upload Job Description (PDF)", type="pdf")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

    if st.button("Evaluate Resume"):
        if job_desc_file and resume_file:
            job_desc_text = extract_text_from_pdf(job_desc_file)
            resume_text = extract_text_from_pdf(resume_file)

            if job_desc_text and resume_text:
                evaluation_result = evaluate_resume(job_desc_text, resume_text)
                st.success("✅ Resume Evaluation Completed:")
                st.write(evaluation_result)
            else:
                st.error("⚠️ Could not extract text from PDFs.")

        else:
            st.error("⚠️ Please upload both a Job Description and a Resume.")

