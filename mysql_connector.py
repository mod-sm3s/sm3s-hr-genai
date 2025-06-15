from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import re
from job_description import  llm

# Setup database connection
# db_uri = "mysql+mysqlconnector://root:iloveareD91%40@localhost/hr_assistant"
db_uri = "mysql+mysqlconnector://root:iloveareD91%40@localhost/company_data"
db = SQLDatabase.from_uri(db_uri)

# Strip markdown-style SQL (```sql ... ```)
def strip_markdown_code(sql: str) -> str:
    return re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()

# Basic validator for safe SELECT-like queries
def is_valid_sql(query: str) -> bool:
    query = query.strip().lower()
    return query.startswith("select") or query.startswith("with") or query.startswith("show") or query.startswith("describe")

# Patch db.run to clean and validate SQL queries
original_run = db.run

def patched_run(sql_cmd: str) -> str:
    cleaned = strip_markdown_code(sql_cmd)
    
    if not is_valid_sql(cleaned):
        print(f"[WARNING] Suspicious SQL (blocked):\n{cleaned}\n")
        raise ValueError(f"Invalid SQL generated: {cleaned}")
    
    return original_run(cleaned)

# Apply the patch
db.run = patched_run

# Create SQL chain
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)



