from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import json
# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# # Job Description Generator
def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
    base_prompt = f"Generate a professional job description for a {title} position."
    base_prompt += "make the section headers to be blue with higher font size, headers like about , job summary , Responsibilities , font type arial "
    base_prompt += "Company name is Smartera"
    base_prompt += "Return **only the formatted job description** — no explanation or intro text. Do NOT include phrases like 'Here’s a job description for...' etc."
    if industry:
        base_prompt += f" The industry is {industry}."
    if responsibilities:
        base_prompt += f" Responsibilities include {responsibilities}."
    if skills:
        base_prompt += f" Required skills: {skills}."
    if experience:
        base_prompt += f" Minimum experience required: {experience} years."

    response = llm.invoke([HumanMessage(content=base_prompt)])
    return response.content

# def generate_job_description(title, industry, responsibilities, skills, experience):
#     prompt = f"""
# Return a job description in the following JSON format (no extra text):
# {{
#   "Job Title": "{title}",
#   "Company": "Smartera",
#   "Industry": "{industry}",
#   "Responsibilities": "{responsibilities}",
#   "Skills": "{skills}",
#   "Experience": "{experience} years",
#   "Full Description": "A full professional summary paragraph."
# }}
#     """
#     response = llm.invoke([HumanMessage(content=prompt)])
#     return response.content

