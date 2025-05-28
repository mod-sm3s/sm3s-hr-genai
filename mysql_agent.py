from crewai import Agent, Task, Crew
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
import mysql.connector

# --- MySQL Querying Function ---
def find_matching_employees(job_description: str) -> str:
    # Connect to DB
    conn = mysql.connector.connect(
        host="127.0.0.1", user="hradmin", password="iloveare", database="hr_assistant"
    )
    cursor = conn.cursor(dictionary=True)

    # Naive skill extraction example
    import re
    skills = re.findall(r'\b\w+\b', job_description.lower())
    placeholders = ' OR '.join([f"skills LIKE '%{s}%'" for s in skills if len(s) > 4])

    query = f"""
    SELECT employee_name, employee_email, skills, years_of_experience, position 
    FROM employees 
    WHERE ({placeholders})
    ORDER BY years_of_experience DESC
    LIMIT 5;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return str(results) if results else "No matching employees found."

# --- LangChain Tool for MySQL ---
from langchain.agents import tool

@tool
def search_employee(job_description: str) -> str:
    """Search for employees in the database matching a job description"""
    return find_matching_employees(job_description)

# --- CrewAI Setup ---
llm = OpenAI(temperature=0)

mysql_tool = Tool.from_function(search_employee)

mysql_agent = Agent(
    role="HR Database Expert",
    goal="Find employees who match the job description",
    backstory="You are an expert in HR and internal databases, tasked with quickly identifying internal candidates.",
    verbose=True,
    tools=[mysql_tool],
    allow_delegation=False,
    llm=llm
)

task = Task(
    description="Given this job description, check for matching employees internally and return their names, emails, and skills.",
    expected_output="A list of matching employees with contact info and skill match explanation.",
    agent=mysql_agent
)

crew = Crew(
    agents=[mysql_agent],
    tasks=[task],
    verbose=True
)

# --- Run Example ---
job_desc = """
We're hiring a software engineer with Python, SQL, and cloud experience.
They should have 3+ years of experience and preferably certifications in AWS.
"""

result = crew.kickoff(inputs={"job_description": job_desc})
print(result)
