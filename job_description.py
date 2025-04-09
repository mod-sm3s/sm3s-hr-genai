from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from fpdf import FPDF
import os
import re
# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# # Job Description Generator
def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
    base_prompt = f"Generate a professional job description for a {title} position."
    base_prompt += "make font color of sections headers to be blue, like About , Job Summary and Responsibilities  , do not return html file , just normal text"
    base_prompt += "Return **only the formatted job description** — no explanation or intro text. Do NOT include phrases like 'Here’s a job description for...' etc."
    base_prompt += "Do not return the Company name Smartera at the beginning of the result"
    #base_prompt += "Do not generate any html elements , "
    base_prompt += "Format the job description using basic HTML with section headers like '<h2 style='color:blue'>About</h2>. Use Arial font. Return only the HTML content."

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
