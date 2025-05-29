from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities.sql_database import SQLDatabase
#from langchain.chains import create_sql_query_chain

db = SQLDatabase.from_uri("mysql+mysqlconnector://root:iloveareD91%40@localhost/hr_assistant")

sql_tool = QuerySQLDataBaseTool(db=db)
