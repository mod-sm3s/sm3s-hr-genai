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
    base_prompt += "make the section headers to be blue with higher font size, headers like about , job summary , Responsibilities , font type arial , do not generate html file , just normal file"
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




class StyledPDF(FPDF):
    def header(self):
        self.add_page()
        pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
        self.set_font("DejaVu", size=14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Job Description", ln=True, align="C")

def render_section_header(pdf, title):
    pdf.ln(5)
    pdf.set_text_color(0, 0, 255)  # Blue
    pdf.set_font("DejaVu", 'B', 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_text_color(0, 0, 0)

def render_paragraph(pdf, text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # remove markdown bold
    lines = text.strip().split('\n')
    for line in lines:
        if line.strip() == "":
            pdf.ln(3)
        else:
            pdf.set_font("DejaVu", size=12)
            pdf.multi_cell(0, 8, line)

def generate_job_pdf(text, filename="job_description.pdf"):
    pdf = StyledPDF()
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)

    # Extract and render by section
    sections = re.split(r'#\s+<font.*?>(.*?)</font>', text)  # Matches section titles
    content_blocks = []

    # First block is the pre-section (often company name), then alternating title/content
    if "**Smartera**" in sections[0]:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Smartera", ln=True)

    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        section_body = sections[i + 1] if (i + 1) < len(sections) else ""
        render_section_header(pdf, section_title)
        render_paragraph(pdf, section_body)

    pdf.output(filename)
    return filename


