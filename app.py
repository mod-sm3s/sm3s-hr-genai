import streamlit as st
from job_description import generate_job_description
from resume_evaluator import evaluate_resume, extract_text_from_pdf
import base64

# Page Configuration
st.set_page_config(page_title="HR AI Assistant", layout="wide")

# Custom CSS for Dark Mode
def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Logo
def add_logo():
    logo_path = "logo.png"  # Add your logo image file
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"<img src='data:image/png;base64,{encoded}' class='logo'>", unsafe_allow_html=True)

add_logo()

# Tabs
tab1, tab2 = st.tabs(["📄 Job Description Generator", "📑 Resume Evaluator"])

# Job Description Generator UI
with tab1:
    st.title("📄 Job Description Generator")
    job_title = st.text_input("Enter Job Title (Required)", "")

    # Optional Inputs
    industry = st.text_input("Industry (Optional)", "")
    responsibilities = st.text_area("Key Responsibilities (Optional)", "")
    skills = st.text_area("Required Skills (Optional)", "")
    experience = st.text_input("Years of Experience (Optional)", "")

    if st.button("Generate Job Description"):
        jd = generate_job_description(job_title, industry, responsibilities, skills, experience)
        st.subheader("📜 Generated Job Description")
        st.write(jd)

# Resume Evaluator UI

with tab2:
    st.title("📑 Resume Evaluator")
    uploaded_job_desc = st.file_uploader("📄 Upload Job Description PDF", type="pdf")
    uploaded_resume = st.file_uploader("📄 Upload Resume PDF", type="pdf")
    inside_tab1, inside_tab2 = st.tabs(["📑 Resume Evaluator Description", "📑 Resume Evaluator Score"])
    with inside_tab2:
        if uploaded_job_desc and uploaded_resume:
            job_desc_text = extract_text_from_pdf(uploaded_job_desc)
            resume_text = extract_text_from_pdf(uploaded_resume)

            skill_comparison = evaluate_resume(job_desc_text, resume_text)

            st.subheader("📊 Skill Match Results")
            for skill, status in skill_comparison.items():
                st.write(f"**{skill.capitalize()}**: {status}")


