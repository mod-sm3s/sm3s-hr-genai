from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase 
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.messages import AIMessage, HumanMessage
from mysql_connector import db, CUSTOM_PROMPT, custom_prompt
from job_description import llm
from langchain.chains.sql_database.prompt import PROMPT

# ✅ Create SQL Chain
# db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True,prompt=CUSTOM_PROMPT,use_query_checker=True )
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True,prompt=custom_prompt,use_query_checker=True )
# ✅ Define State
class AgentState(TypedDict):
    input: str
    intent: Optional[str]
    response: Optional[str]

# 🧠 Intent Classification
def route_intent(state: AgentState):
    input_text = state["input"]
    intent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intent classifier. Your options are: [sql, chat]. Decide what this input is about."),
        ("human", "{input}")
    ])
    chain = intent_prompt | llm | (lambda msg: msg.content.lower().strip())
    intent = chain.invoke({"input": input_text})
    return {"intent": intent}

# 💬 Chat Handler
def handle_chat(state: AgentState):
    response = llm.invoke([HumanMessage(content=state["input"])])
    return {"response": response.content}

# 🗄️ SQL Handler
def handle_sql(state: AgentState):
    response = db_chain.run(state["input"])
    return {"response": response}

# ⚙️ Tool Router
def route_tools(state: AgentState):
    intent = state.get("intent", "")
    if intent == "sql":
        return "sql"
    return "chat"

# 🧱 Build LangGraph
# 🧱 Build LangGraph
builder = StateGraph(AgentState)

# 🆕 Renamed node to 'classify_intent'
builder.add_node("classify_intent", RunnableLambda(route_intent))
builder.add_node("chat", RunnableLambda(handle_chat))
builder.add_node("sql", RunnableLambda(handle_sql))

builder.set_entry_point("classify_intent")
builder.add_conditional_edges("classify_intent", route_tools, {
    "sql": "sql",
    "chat": "chat"
})
builder.add_edge("chat", END)
builder.add_edge("sql", END)


graph = builder.compile()

# 🧪 CLI loop
if __name__ == "__main__":
    print("💬 Start chatting with your AI agent (type 'exit' to quit):")
    while True:
        user_input = input("🧠 You: ")
        if user_input.lower() == "exit":
            break
        result = graph.invoke({"input": user_input})
        print("📊 Result:\n", result.get("response", "[No response]"))
