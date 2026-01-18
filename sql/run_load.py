import duckdb
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "saas.db")

schema_path = os.path.join(project_root, "sql", "schema.sql")
load_path = os.path.join(project_root, "sql", "load_data.sql")

con = duckdb.connect(db_path)

def exec_sql_file(path):
    with open(path, "r") as f:
        sql = f.read()
    for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
        con.execute(stmt + ";")

print("Running schema...")
exec_sql_file(schema_path)
print("Schema created.")

print("Running data load...")
exec_sql_file(load_path)
print("Data loaded.")

con.close()
print(f"DB READY at {db_path}")
