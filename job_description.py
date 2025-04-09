from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from fpdf import FPDF
import os
import re
# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# # Job Description Generator
#def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
def generate_job_description(title,company, industry="", responsibilities="", skills="", experience=""):
    base_prompt = f"Generate a professional job description for a {title} position and {company}."
    base_prompt = f"Company name: {company}. "
    base_prompt += "make the section headers to be blue , headers like About , Job Summary , Responsibilities  , do not generate html file , just normal file"
    base_prompt += "Return **only the formatted job description** — no explanation or intro text. Do NOT include phrases like 'Here’s a job description for...' etc."
    base_prompt += "Do not return the Company name Smartera at the beginning of the result"
    base_prompt += "Do not write font type or size in result"
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





