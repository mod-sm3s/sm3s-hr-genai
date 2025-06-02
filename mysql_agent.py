from crewai import Agent, Crew, Task
from mysql_connector import sql_tool
from crewai.tools import tool
from job_description import generate_job_description, llm


llm = llm


@tool("Employee SQL Query Tool")
def query_employee_data(query: str) -> str:
    """Executes a SQL query to retrieve employee data."""
    return sql_tool.run(query)
db_agent = Agent(
    role="HR Database Analyst",
    goal="Identify suitable employees from the database based on job requirements",
    backstory="You are an expert HR analyst with access to employee data stored in a MySQL database. You help HR teams find the best candidates internally.",
    tools=[sql_tool],
    llm=llm,
    verbose=True,
)

def build_query_from_job_description(job_description: str) -> str:
    return f"""
SELECT * FROM employees
WHERE MATCH(skills) AGAINST('{job_description}' IN NATURAL LANGUAGE MODE)
   OR MATCH(position, department) AGAINST('{job_description}' IN NATURAL LANGUAGE MODE)
   OR years_experience >= 2;
 """
job_description = generate_job_description(job_title="software engineer")
sql_query = build_query_from_job_description(job_description)

match_task = Task(
    description=f"Run the following SQL query using the QuerySQLDataBaseTool:\n\n{sql_query}",
    expected_output="A list of employee names, emails, and positions who match the given skills (Python, SQL, data analysis).",
    agent=db_agent
)
# task = Task(
#     description="Find employees who match the following job requirements: strong Python skills, experience with SQL and data analysis.",
#      expected_output="A list of employee names, emails, and positions who match the given skills (Python, SQL, data analysis).",
#     agent=db_agent
# )


# Run the agent as a crew
crew = Crew(
    agents=[db_agent],
    tasks=[match_task],
    verbose=True
)

# Execute
result = crew.kickoff()

print("=== Result ===")
print(result)
