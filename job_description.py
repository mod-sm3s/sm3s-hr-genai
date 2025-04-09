from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Initialize Gemini 2.0 Flash Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

# # Job Description Generator
# def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
#     base_prompt = f"Generate a professional job description for a {title} position."
#     base_prompt += "Company name is Smartera"
#     base_prompt += ""
#     if industry:
#         base_prompt += f" The industry is {industry}."
#     if responsibilities:
#         base_prompt += f" Responsibilities include {responsibilities}."
#     if skills:
#         base_prompt += f" Required skills: {skills}."
#     if experience:
#         base_prompt += f" Minimum experience required: {experience} years."

#     response = llm.invoke([HumanMessage(content=base_prompt)])
#     return response.content

def generate_job_description(title, industry="", responsibilities="", skills="", experience=""):
    base_prompt = f"""
You are a helpful AI assistant. Generate a professional job description in **Markdown format** for a **{title}** position.
Return **only the formatted job description** — no explanation or intro text. Do NOT include phrases like "Here’s a job description for..." etc.

Use the following structure:
The company name is **Smartera**.
{f"The industry is **{industry}**." if industry else ""}
{f"Responsibilities include: {responsibilities}." if responsibilities else ""}
{f"Required skills: {skills}." if skills else ""}
{f"Minimum experience required: {experience} years." if experience else ""}

Break it into the following **Markdown sections**:
- 📌 Job Title
- 🏢 Company
- 🌐 Industry
- 💼 Responsibilities
- 🧠 Required Skills
- 📅 Experience
- 📝 Full Job Description
    """.strip()

    response = llm.invoke([HumanMessage(content=base_prompt)])
    return response.content

