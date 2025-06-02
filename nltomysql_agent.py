from crewai import Agent, Crew, Task
from mysql_connector import nlsql
from job_description import llm

# db_agent = Agent(
#     role="HR Database Analyst",
#     goal="Identify suitable employees from the database based on job requirements",
#     backstory="You are an expert HR analyst with access to employee data stored in a MySQL database. You help HR teams find the best candidates internally.",
#     tools=[nlsql],
#     llm=llm,
#     verbose=True,
# )

# task = Task(
#     prompt="List all employees who joined after 2018",
#     description="Query employees who joined after 2018",
#     expected_output="List of employee records with joined_since > 2018-01-01",
#     agent=db_agent  
# )

# crew = Crew(
#     agents=[db_agent],
#     tasks=[task],
#     verbose=True,
# )

# result = crew.kickoff()
# print(result)
from crewai import Agent, Crew, Task
from mysql_connector import nlsql  # your NL2SQL tool
from job_description import llm    # your LLM instance

# Define a simple system prompt to control agent behavior
system_prompt = """
You are an agent that can only use one tool: NL2SQLTool.

When you want to use the tool, respond exactly in this format:

Thought: <your thoughts>
Action: NL2SQLTool
Action Input: {"nl_query": "List all employees"}

Wait for the tool output before giving the final answer.

If you want to give a final answer, respond with:

Thought: <your final thoughts>
Final Answer: <your answer>
"""


db_agent = Agent(
    role="HR Database Analyst",
    goal="Identify suitable employees from the database based on job requirements",
    backstory="You are an expert HR analyst with access to employee data stored in a MySQL database. You help HR teams find the best candidates internally.",
    tools=[nlsql],
    llm=llm,
    verbose=True,
)

# Create Task with required fields
task = Task(
    prompt={"nl_query": "List all employees"},
    description="Query employees who joined after 2018",
    expected_output="A table of employee data with all columns",
    agent=db_agent 
)


# Create Crew with the agent and the task
crew = Crew(
    agents=[db_agent],
    tasks=[task],
    verbose=True
)

# Run
result = crew.kickoff()
print(result)
