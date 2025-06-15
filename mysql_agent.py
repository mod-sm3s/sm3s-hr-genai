# graph_agent.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from job_description import generate_job_description
from mysql_connector import db_chain

# Define the structure passed between nodes
class AgentState(TypedDict, total=False):
    job_title: str
    years_experience: Optional[str]
    skills: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    job_description: str
    query_results: str

# Step 1: Generate Job Description
def node_generate_description(state: AgentState) -> AgentState:
    jd = generate_job_description(
        job_title=state["job_title"],
        years_experience=state.get("years_experience"),
        skills=state.get("skills"),
        description=state.get("description"),
        industry=state.get("industry"),
    )
    return {**state, "job_description": jd}

# Step 2: Query Internal Employee DB
# def node_query_database(state: AgentState) -> AgentState:
#     prompt = f"""
# Find all employees in the database whose skills and experience match the following job description:

# \"\"\"{state['job_description']}\"\"\"

# List their names, emails, positions, and departments.
# """
#     result = db_chain.run(prompt)
#     return {**state, "query_results": result}
def node_query_database(state: AgentState) -> AgentState:
    prompt = f"""
You are an expert SQL agent. Based on the following job description, find internal candidates who are a good match, 
even if they do not meet every single requirement exactly. Prioritize candidates with most of the relevant skills 
and sufficient years of experience.

Job Description:
\"\"\"{state['job_description']}\"\"\"

Instructions:
- Use OR conditions for matching skills instead of AND.
- Prefer candidates with at least some relevant experience (e.g., 3+ years).
- Retrieve the top 5 candidates based on the number of matching skills.
- Return their names, emails, positions, and departments.
"""
    
    result = db_chain.run(prompt)
    return {**state, "query_results": result}

# Build graph: generate → query → finish
workflow = StateGraph(AgentState)
workflow.add_node("generate_description", node_generate_description)
workflow.add_node("query_database", node_query_database)
workflow.set_entry_point("generate_description")
workflow.add_edge("generate_description", "query_database")
workflow.add_edge("query_database", END)

graph_app = workflow.compile()

# Runner function
def run_internal_match_flow(job_title: str,
                            years_experience: Optional[str] = None,
                            skills: Optional[str] = None,
                            description: Optional[str] = None,
                            industry: Optional[str] = None) -> AgentState:
    result = graph_app.invoke({
        "job_title": job_title,
        "years_experience": years_experience,
        "skills": skills,
        "description": description,
        "industry": industry
    })
   # print("🔹 Job description:\n", result["job_description"])
    print("✅ Matched internal candidates:\n", result["query_results"])
    return result
