# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage
# import streamlit as st
# from fpdf import FPDF
# import re
# import os

# # --- Initialize Gemini ---
# api_key = "AIzaSyDwZPIHsn8K0FZvwQHLHMeX4VRNv5sfJ7M"
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     temperature=0.7,
#     google_api_key=api_key
# )

# # --- Function to generate job description ---
# def generate_job_description(title, industry, responsibilities, skills, experience):
#     prompt = f"""Generate a professional job description for a {title} role.

# Include these sections:
# - **About the Role**
# - **Key Responsibilities**
# - **Required Skills**
# - **Experience Required**

# Use markdown-style formatting. Do NOT include intro text or company name.

# """
#     if industry:
#         prompt += f"\nIndustry: {industry}"
#     if responsibilities:
#         prompt += f"\nKey responsibilities include: {responsibilities}"
#     if skills:
#         prompt += f"\nImportant skills: {skills}"
#     if experience:
#         prompt += f"\nMinimum experience required: {experience} years"

#     try:
#         response = llm.invoke([HumanMessage(content=prompt)])
#         return response.content.strip()
#     except Exception as e:
#         return f"[ERROR] {str(e)}"

# # --- Streamlit page setup ---
# st.set_page_config(page_title="Job Description Generator", layout="wide")
# st.title("📄 Job Description Generator")

# # --- User input ---
# job_title = st.text_input("Enter Job Title (Required)", "")
# industry = st.text_input("Industry (Optional)", "")
# responsibilities = st.text_area("Key Responsibilities (Optional)", "")
# skills = st.text_area("Required Skills (Optional)", "")
# experience = st.text_input("Years of Experience (Optional)", "")

# # --- State storage ---
# if "job_desc" not in st.session_state:
#     st.session_state.job_desc = ""
# if "pdf_path" not in st.session_state:
#     st.session_state.pdf_path = ""

# # --- Generate button ---
# if st.button("Generate Job Description"):
#     if not job_title.strip():
#         st.error("⚠️ Job Title is required.")
#     else:
#         with st.spinner("Generating with Gemini..."):
#             job_desc = generate_job_description(job_title, industry, responsibilities, skills, experience)
#             if "[ERROR]" in job_desc or not job_desc.strip():
#                 st.error("❌ Failed to generate job description. Try again or simplify your input.")
#             else:
#                 st.session_state.job_desc = job_desc

#                 # Show job description
#                 st.markdown("""
#                 <style>
#                 .job-box {
#                     background-color: #fff;
#                     padding: 20px;
#                     border-radius: 12px;
#                     box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#                     font-family: 'Segoe UI', sans-serif;
#                 }
#                 </style>
#                 """, unsafe_allow_html=True)

#                 st.markdown('<div class="job-box">', unsafe_allow_html=True)
#                 st.markdown(job_desc, unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#                 # Create PDF
#                 clean_text = re.sub(r'(\*\*|__|\*|#+)', '', job_desc)
#                 pdf = FPDF()
#                 pdf.add_page()
#                 pdf.set_font("Arial", size=12)
#                 pdf.multi_cell(190, 10, clean_text)
#                 pdf_path = "job_description.pdf"
#                 pdf.output(pdf_path)
#                 st.session_state.pdf_path = pdf_path
#                 st.success("✅ Job description generated!")

# # --- Download button ---
# if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
#     with open(st.session_state.pdf_path, "rb") as f:
#         st.download_button("📥 Download PDF", f, file_name="job_description.pdf", mime="application/pdf")


import streamlit as st
import traceback

try:
    st.title("🧪 Testing Streamlit")
    st.text_input("Try typing something")
    # Add more of your real logic here
except Exception as e:
    st.error("Something went wrong!")
    st.text(str(e))
    st.text(traceback.format_exc())






