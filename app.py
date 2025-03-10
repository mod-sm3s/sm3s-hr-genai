import streamlit as st
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import PyPDF2
from fpdf import FPDF

# Initialize LangChain Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key="your-api-key-here",
    convert_system_message_to_human=True
)

# Function to generate a job description
def generate_job_description(title="Banking Associate", department="Retail Banking", seniority="Mid-level", 
                             location="Remote/On-site", employment_type="Full-time", salary_range="Competitive",
                             responsibilities=None, skills=None, experience="3+ years", 
                             qualifications="Bachelor's degree in Finance or related field",
                             benefits="Health insurance, performance bonuses, training programs"):
    if responsibilities is None:
        responsibilities = ["Assist customers with banking transactions.",
                            "Ensure compliance with financial regulations.",
                            "Analyze client financial needs and provide suitable solutions."]
    if skills is None:
        skills = ["Customer Service", "Financial Analysis", "Risk Management", "Attention to Detail"]
    
    job_description = f"""
    **Job Title:** {title}
    **Department:** {department}
    **Seniority Level:** {seniority}
    **Location:** {location}
    **Employment Type:** {employment_type}
    **Salary Range:** {salary_range}
    **Years of Experience:** {experience}
    **Qualifications:** {qualifications}
    
    **Key Responsibilities:**
    - {responsibilities[0]}
    - {responsibilities[1]}
    - {responsibilities[2]}
    
    **Required Skills:**
    - {skills[0]}
    - {skills[1]}
    - {skills[2]}
    
    **Company Benefits:**
    {benefits}
    """
    return job_description

# Function to evaluate a resume against a job description
def evaluate_resume(job_description, resume_text):
    prompt = f"""Compare the following job description and resume. 
    Identify how well the resume matches the job based on skills, experience, and qualifications.
    
    **Job Description:**
    {job_description}
    
    **Resume:**
    {resume_text}
    
    Provide a score (1-10) and feedback.
    """
    
    response = llm([HumanMessage(content=prompt)])
    return response.content

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Streamlit UI Design
st.set_page_config(page_title="HR AI System", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #00FFEA;
        }
        .stTextInput>div>div>input {
            background-color: #222;
            color: #00FFEA;
        }
        .stButton>button {
            background-color: #00FFEA;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Tabs for Job Description Generator & Resume Evaluator
tabs = st.tabs(["🔹 Job Description Generator", "📄 Resume Evaluator"])

with tabs[0]:
    st.header("Generate Job Description")
    title = st.text_input("Job Title", "Banking Associate")
    department = st.text_input("Department", "Retail Banking")
    seniority = st.selectbox("Seniority Level", ["Junior", "Mid-level", "Senior", "Lead"], index=1)
    location = st.text_input("Location", "Remote/On-site")
    employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Internship"], index=0)
    experience = st.text_input("Years of Experience", "3+ years")
    responsibilities = st.text_area("Key Responsibilities", "Assist customers with banking transactions.")
    skills = st.text_area("Required Skills", "Customer Service, Financial Analysis")
    qualifications = st.text_area("Qualifications", "Bachelor's degree in Finance or related field")
    benefits = st.text_area("Company Benefits", "Health insurance, performance bonuses")
    
    if st.button("Generate Job Description"):
        jd_output = generate_job_description(title, department, seniority, location, employment_type, "Competitive",
                                             [responsibilities], [skills], experience, qualifications, benefits)
        st.text_area("Generated Job Description", jd_output, height=300)
    
    if st.button("Save as PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(190, 10, jd_output)
        pdf.output("job_description.pdf")
        st.success("PDF saved successfully!")

with tabs[1]:
    st.header("Resume Evaluator")
    job_desc_file = st.file_uploader("Upload Job Description PDF", type=["pdf"])
    resume_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
    
    if st.button("Evaluate Resume"):
        if job_desc_file and resume_file:
            job_desc_text = extract_text_from_pdf(job_desc_file)
            resume_text = extract_text_from_pdf(resume_file)
            evaluation_result = evaluate_resume(job_desc_text, resume_text)
            st.text_area("Evaluation Result", evaluation_result, height=300)
        else:
            st.error("Please upload both the job description and resume PDFs.")

