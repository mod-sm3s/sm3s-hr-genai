# mysql_connector.py
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import re
from job_description import  llm
from langchain.prompts import PromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX

CUSTOM_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template="""
You are a MySQL expert. Given a question and the database schema, write a correct SQL query.

If the user asks for employees with a skill like "Excel", join `employees`, `employee_skills`, and `skills` tables.

Use this logic:
- employees.employee_id ↔ employee_skills.employee_id
- employee_skills.skill_id ↔ skills.skill_id

Only use relevant columns.

{table_info}

Question: {input}
SQLQuery:
""".strip() + PROMPT_SUFFIX
)

custom_prompt = PromptTemplate.from_template("""
You are an expert in translating natural language questions into SQL queries.

Use ONLY the following schema:
employees(employee_id, name, email, years_experience, department_id)
skills(skill_id, skill_name)
employee_skills(employee_id, skill_id)

Do NOT assume table names or column names. Use only the ones shown above.

Question: {input}
SQLQuery:
""")

db_uri = "mysql+mysqlconnector://root:iloveareD91%40@localhost/company_data"
db = SQLDatabase.from_uri(db_uri,include_tables=["employees", "employee_skills", "skills","departments"])

def strip_markdown_code(sql: str) -> str:
    return re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()

def is_valid_sql(query: str) -> bool:
    query = query.strip().lower()
    return query.startswith(("select", "with", "show", "describe"))

# Patch db.run
original_run = db.run
def patched_run(sql_cmd: str) -> str:
    cleaned = strip_markdown_code(sql_cmd)
    if not is_valid_sql(cleaned):
        raise ValueError(f"Invalid SQL generated: {cleaned}")
    return original_run(cleaned)
db.run = patched_run


# db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True, prompt=CUSTOM_PROMPT)