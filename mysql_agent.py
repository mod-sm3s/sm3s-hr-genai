from crewai import Agent, Task, Crew
from langchain.agents import Tool
from mysql_connector import sql_tool
from job_description import generate_job_description, llm

db_agent = Agent(
    role="Employee Matcher",
    goal="Identify employees from the database who fit a given job description",
    backstory="Expert in HR analytics and SQL. Efficient at understanding job profiles and searching talent databases.",
    verbose=True,
    tools=[sql_tool],  
    llm = llm
)
# db_agent = Agent(
#     role="Employee Matcher",
#     goal="Identify employees from the database who fit a given job description",
#     backstory="Expert in HR analytics and SQL. Efficient at understanding job profiles and searching talent databases.",
#     verbose=True,
#     tools=[sql_tool], 
#     #tools=[Tool.from_function(sql_tool.run, name="QuerySQLDataBaseTool", description="Query employee data.")],
# )

def build_query_from_job_description(job_description: str) -> str:
    return f"""
SELECT * FROM employees
WHERE MATCH(skills) AGAINST('{job_description}' IN NATURAL LANGUAGE MODE)
   OR MATCH(position, department) AGAINST('{job_description}' IN NATURAL LANGUAGE MODE)
   OR years_experience >= 2;
"""  # Simplified; you can add NLP-to-SQL via LLM too

# job_description = """...output from generate_job_description..."""  # Plug the output here
job_description = generate_job_description(job_title="software engineer")
sql_query = build_query_from_job_description(job_description)

match_task = Task(
    description=f"Run the following SQL query using the QuerySQLDataBaseTool:\n\n{sql_query}",
    agent=db_agent
)


crew = Crew(
    agents=[db_agent],
    tasks=[match_task],
    verbose=True
)

crew.kickoff()
