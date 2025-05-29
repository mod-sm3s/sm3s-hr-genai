from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Gemini 2.0 Flash setup (replace with your actual key)
api_key = "AIzaSyDwZPIHsn8K0FZvwQHLHMeX4VRNv5sfJ7M"
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.7, google_api_key=api_key)

def generate_job_description(job_title: str, years_experience: str = None,
                              skills: str = None, description: str = None, industry: str = None) -> str:
    prompt_template = PromptTemplate(
        input_variables=["job_title", "years_experience", "skills", "description", "industry"],
        template="""
You are a professional HR expert. Generate a detailed and attractive job description for the following job:

Job Title: {job_title}
Years of Experience: {years_experience}
Required Skills: {skills}
Additional Description: {description}
Industry: {industry}

The job description should include:
- A short intro about the company and the role
- Responsibilities
- Requirements
- Benefits
Make it professional and clear.
"""
    )

    prompt = prompt_template.format(
        job_title=job_title,
        years_experience=years_experience or "Not specified",
        skills=skills or "Not specified",
        description=description or "None",
        industry=industry or "General"
    )

    return llm.invoke(prompt).content
