import streamlit as st
from job_description import generate_job_description
from resume_evaluator import resume_description, resume_score, extract_text_from_pdf
import base64
from fpdf import FPDF
import pdfkit
import tempfile
from jinja2 import Template
from pathlib import Path
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

tab1, tab2 = st.tabs(["📄 Job Description Generator", "📑 Resume Evaluator"])

# Job Description Generator UI
with tab1:
    st.subheader("Generate a Job Description")
    st.markdown("""
    Provide the job title (required) and any other optional details. The generator will produce a clean, professional job description with separate sections, similar to [smartera3s.com](https://www.smartera3s.com/).
    """)

    with st.form("job_form"):
        job_title = st.text_input("Job Title *")
     #   company = st.text_input("Company Name")
        responsibilities = st.text_area("Responsibilities")
        qualifications = st.text_area("Qualifications")
        benefits = st.text_area("Benefits")
        location = st.text_input("Location", placeholder="e.g. Remote / San Francisco")
        employment_type = st.selectbox("Employment Type", ["", "Full-time", "Part-time", "Contract", "Internship", "Freelance"])

        submitted = st.form_submit_button("Generate Job Description")

    jd_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          font-family: 'Segoe UI', sans-serif;
          margin: 40px;
          line-height: 1.6;
          color: #333;
        }
        h2 {
          color: #1f77b4;
          border-bottom: 2px solid #eaeaea;
          padding-bottom: 5px;
        }
        .section {
          margin-bottom: 30px;
        }
        strong {
          color: #000;
        }
      </style>
    </head>
    <body>
      Generate a professional job description for the role: "{{ job_title }}".

        {% if company %}
        The company name is {{ company }}.
        {% endif %}
        {% if responsibilities %}
        Here are some suggested responsibilities: {{ responsibilities }}.
        {% endif %}
        {% if qualifications %}
        Here are some suggested qualifications: {{ qualifications }}.
        {% endif %}
        {% if benefits %}
        These are the benefits offered: {{ benefits }}.
        {% endif %}
        {% if location %}
        The position is located at: {{ location }}.
        {% endif %}
        {% if employment_type %}
        This is a {{ employment_type }} role.
        {% endif %}

Please format the output with clearly separated sections and use a visually appealing layout.

    </body>
    </html>
    """)

    if submitted:
        if not job_title:
            st.warning("Please enter at least a Job Title.")
        else:
            html_content = jd_template.render(
                job_title=job_title,
                responsibilities=responsibilities,
                qualifications=qualifications,
                benefits=benefits,
                location=location,
                employment_type=employment_type
            )

            st.markdown("---")
            st.subheader("📋 Generated Job Description")
            st.components.v1.html(html_content, height=600, scrolling=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                pdfkit.from_string(html_content, tmp_pdf.name)
                with open(tmp_pdf.name, "rb") as f:
                    st.download_button(
                        label="📄 Download PDF",
                        data=f,
                        file_name=f"{job_title.replace(' ', '_')}_Job_Description.pdf",
                        mime="application/pdf"
                    )

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


