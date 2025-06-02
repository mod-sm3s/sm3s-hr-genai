# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# from langchain_community.utilities.sql_database import SQLDatabase
# #from langchain.chains import create_sql_query_chain

# db = SQLDatabase.from_uri("mysql+mysqlconnector://root:iloveareD91%40@localhost/hr_assistant")

# sql_tool = QuerySQLDataBaseTool(db=db)

from crewai_tools import MySQLSearchTool
# # Initialize the tool with the database URI and the target table name
# sql_tool = MySQLSearchTool(
#     db_uri="mysql://root:iloveareD91%40@localhost/hr_assistant",
#     table_name='employees',
# )

# print(sql_tool.run('select * from employees'))
# nlsql = NL2SQLTool(db_uri="mysql://root:iloveareD91%40@localhost/hr_assistant")

# from sqlalchemy import create_engine, inspect
# from crewai_tools import NL2SQLTool

# # Connect to your database
# engine = create_engine("mysql://root:iloveareD91%40@localhost/hr_assistant")
# inspector = inspect(engine)

# # Extract tables and columns
# schema = {}
# for table_name in inspector.get_table_names():
#     columns = inspector.get_columns(table_name)
#     schema[table_name] = [col["name"] for col in columns]

# nlsql = NL2SQLTool(db_uri="mysql://root:iloveareD91%40@localhost/hr_assistant", schema=schema)
# print("Schema extracted:", schema)
from crewai_tools import NL2SQLTool
import mysql.connector

# === 1. Connect to MySQL ===
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="iloveareD91@",
    database="hr_assistant"
)
cursor = connection.cursor()

# === 2. Detect schema: tables + columns ===
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

schema = {}
for table in tables:
    cursor.execute(f"SHOW COLUMNS FROM {table}")
    schema[table] = [row[0] for row in cursor.fetchall()]

print("✅ Detected Schema:")
for t, cols in schema.items():
    print(f"- {t}: {cols}")

# === 3. Initialize NL2SQLTool with JUST table names ===
nl2sql_tool = NL2SQLTool(
    db_uri="mysql://root:iloveareD91%40@localhost/hr_assistant",
    tables=schema  # ✅ Must be a list of table names
)

# === 4. Example natural language query ===
nl_query = "List all employees who joined after 2018"

# === 5. Get SQL from NL ===
sql_query = nl2sql_tool.run(nl_query)
print("\n🧠 Generated SQL:\n", sql_query)

# === 6. Run SQL on DB ===
try:
    cursor.execute(sql_query)
    results = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]

    print("\n📊 Results:")
    print(column_names)
    for row in results:
        print(row)

except mysql.connector.Error as err:
    print("❌ SQL Error:", err)
    print("Query was:", sql_query)

# === 7. Cleanup ===
cursor.close()
connection.close()

