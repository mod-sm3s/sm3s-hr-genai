from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os
import re
# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# # Job Description Generator
def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
    base_prompt = f"Generate a professional job description for a {title} position."
    base_prompt += "return font color of headers of sections as blue, like About , Job Summary and Responsibilities  , do not return html elements , just normal text"
    base_prompt += "Return **only the formatted job description** — no explanation or intro text. Do NOT include phrases like 'Here’s a job description for...' etc."
    base_prompt += "Do not return the Company name Smartera at the beginning of the result"
    base_prompt += "Make sections separate and aligned"
   
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
