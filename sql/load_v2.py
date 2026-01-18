import duckdb
import pandas as pd

# Load CSVs using pandas
users = pd.read_csv("../data/raw/users.csv")
subscriptions = pd.read_csv("../data/raw/subscriptions.csv")
events = pd.read_csv("../data/raw/events.csv")
payments = pd.read_csv("../data/raw/payments.csv")

# Connect to DB
con = duckdb.connect("../saas.db")

# Register DataFrames as tables
con.execute("DROP TABLE IF EXISTS users;")
con.execute("DROP TABLE IF EXISTS subscriptions;")
con.execute("DROP TABLE IF EXISTS events;")
con.execute("DROP TABLE IF EXISTS payments;")

con.register("users_df", users)
con.register("subscriptions_df", subscriptions)
con.register("events_df", events)
con.register("payments_df", payments)

# Create actual DuckDB tables
con.execute("CREATE TABLE users AS SELECT * FROM users_df;")
con.execute("CREATE TABLE subscriptions AS SELECT * FROM subscriptions_df;")
con.execute("CREATE TABLE events AS SELECT * FROM events_df;")
con.execute("CREATE TABLE payments AS SELECT * FROM payments_df;")

print("Database loaded successfully using pandas!")
con.close()
