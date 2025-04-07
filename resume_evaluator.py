from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import PyPDF2

# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Extract skills from text
def extract_skills(text):
    prompt = f"Extract all skills (technical and soft) from the following text:\n{text}\nReturn as a comma-separated list."
    response = llm.invoke([HumanMessage(content=prompt)])
    return set(response.content.lower().split(","))

# Compare job description and resume skills
def resume_score(job_desc_text, resume_text):
    job_skills = extract_skills(job_desc_text)
    resume_skills = extract_skills(resume_text)

    matched_skills = job_skills.intersection(resume_skills)
    missing_skills = job_skills - resume_skills

    # Format output
    skill_comparison = {
        skill: "✅ Yes" if skill in matched_skills else "❌ No"
        for skill in job_skills
    }

    return skill_comparison

def resume_description(job_desc_text, resume_text):
    prompt = f"Evaluate the resume against the job description.\n\nJob Description:\n{job_desc_text}\n\nResume:\n{resume_text}\n\nHow well does this candidate fit?"
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
