import os
import json
import uuid
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from job_description import llm
# === CONFIG ===

CANDIDATE_FILE = "candidates.json"

# === UTILITIES ===
def read_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()

def load_candidates():
    if not os.path.exists(CANDIDATE_FILE):
        return {}
    with open(CANDIDATE_FILE, "r") as f:
        return json.load(f)

def save_candidates(data):
    with open(CANDIDATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_next_candidate_id(existing_data):
    return f"candidate_{len(existing_data) + 1}"

# === PROMPT TEMPLATE ===
prompt_template = PromptTemplate.from_template("""
You are an HR assistant. Given a job description and a candidate's resume, do the following:
1. Score the resume from 0 to 100 based on how well it fits the job.
2. Extract structured information as JSON with the following keys:
   - name, email, phone, years_of_experience, last_employers (list), year_of_grad,
     skills (list), education (list), certificates (list), gender, address,
     linkedin, github, current_position, languages (list), score

If a value is missing in the resume, leave it as null.

--- JOB DESCRIPTION ---
{job_description}

--- RESUME ---
{resume}
""")

# === MAIN FUNCTION ===
def evaluate_resume(resume_path: str, jd_path: str):
    resume_text = read_pdf_text(resume_path)
    jd_text = read_pdf_text(jd_path)

    prompt = prompt_template.format(resume=resume_text, job_description=jd_text)
    response = llm.invoke(prompt)

    parser = JsonOutputParser()
    try:
        structured = parser.invoke(response)
    except Exception:
        import ast
        structured = ast.literal_eval(response.content)

    candidates = load_candidates()
    candidate_id = get_next_candidate_id(candidates)
    candidates[candidate_id] = structured
    save_candidates(candidates)

    print(f"✅ {candidate_id} evaluated and added.")
    return candidate_id, structured

# === RUN SCRIPT ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--resume", help="Path to a single resume PDF")
    group.add_argument("--resume_folder", help="Folder path containing multiple resume PDFs")
    parser.add_argument("--jd", required=True, help="Path to job description PDF")
    args = parser.parse_args()

    evaluate_resume(args.resume, args.jd)
