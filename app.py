import streamlit as st
from job_description import generate_job_description
from resume_evaluator import resume_description, resume_score, extract_text_from_pdf
import base64
from fpdf import FPDF
import os
import re
import json
# Page Configuration
st.set_page_config(page_title="HR AI Assistant", layout="wide")
def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Logo
def add_logo(): 
    logo_path = "logo-sm.png"
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(f"<img src='data:image/png;base64,{encoded}' class='logo'>", unsafe_allow_html=True)

add_logo()

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", size=14)
        self.cell(0, 10, "Job Description", ln=True, align="C")

def strip_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.strip()

def create_pdf(data, filename="job_description.pdf"):
    pdf = PDF()
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.add_page()

    for section, value in data.items():
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, f"{section}:\n{strip_markdown(value)}\n")

    pdf.output(filename)
    return filename



# Custom CSS for Dark Mode


# Tabs
tab1, tab2 = st.tabs(["📄 Job Description Generator", "📑 Resume Evaluator"])

# Job Description Generator UI
with tab1:
    st.title("📝 Job Description Generator")
    pdf_path = ""
    with st.form("job_form"):
        title = st.text_input("Job Title")
        industry = st.text_input("Industry (Optional)")
        responsibilities = st.text_area("Responsibilities  (Optional)")
        skills = st.text_area("Skills")
        experience = st.text_input("Minimum Experience (years)  (Optional)")
        submitted = st.form_submit_button("Generate Description")

    if submitted:
        with st.spinner("Generating with Gemini..."):
            data = generate_job_description(title, industry, responsibilities, skills, experience)
    
        st.success("✅ Job Description Generated")
    
        # Display each section cleanly
        for section, value in data.items():
            st.subheader(section)
            st.write(value)
    
        # Create PDF
        pdf_path = create_pdf(data)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=pdf_path, mime="application/pdf")
    
    # Streamlit download button
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Job Description PDF", f, file_name=pdf_file, mime="application/pdf")
        # Resume Evaluator UI

with tab2:
     st.title("📑 Resume Evaluator")
     uploaded_job_desc = st.file_uploader("📄 Upload Job Description PDF", type="pdf")
     uploaded_resume = st.file_uploader("📄 Upload Resume PDF", type="pdf")
     inside_tab1, inside_tab2 = st.tabs(["📑 Resume Evaluator Description", "📑 Resume Evaluator Score"])
     with inside_tab1:
         if uploaded_job_desc and uploaded_resume:
             job_desc_text = extract_text_from_pdf(uploaded_job_desc)
             resume_text = extract_text_from_pdf(uploaded_resume)
             with st.spinner("Wait for it...", show_time=True):
                 desc = resume_description(job_desc_text, resume_text)
                 st.subheader("📊 Skill Descriptions")
                 st.write(desc)
                 st.success("Done!")
 
     with inside_tab2:
         if uploaded_job_desc and uploaded_resume:
             job_desc_text = extract_text_from_pdf(uploaded_job_desc)
             resume_text = extract_text_from_pdf(uploaded_resume)           
             skill_comparison = resume_score(job_desc_text, resume_text)
             matched_skills = [skill for skill, status in skill_comparison.items() if "Yes" in status]
             missing_skills = [skill for skill, status in skill_comparison.items() if "No" in status]
             st.markdown("<h3>✅ Matched Skills</h3>", unsafe_allow_html=True)
             st.markdown('<div class="skill-box">' + ''.join(f'<span class="skill-tag matched">{skill}</span>' for skill in matched_skills) + '</div>', unsafe_allow_html=True)
             st.markdown("<h3>❌ Missing Skills</h3>", unsafe_allow_html=True)
             st.markdown('<div class="skill-box">' + ''.join(
    f'<span class="skill-tag missing">{skill}</span>' for skill in missing_skills
) + '</div>', unsafe_allow_html=True)
           #  st.subheader("📊 Skill Match Results")
             # for skill, status in skill_comparison.items():
             #     st.write(f"**{skill.capitalize()}**: {status}")


