import duckdb

con = duckdb.connect("../saas.db")

print("=== Table Counts ===")
for t in ["users", "subscriptions", "events", "payments"]:
    print(f"{t}: {con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}")

print("\n=== Plan Distribution ===")
print(con.execute("""
SELECT plan, COUNT(*) 
FROM subscriptions 
GROUP BY plan
ORDER BY plan
""").fetchdf())

print("\n=== Churned Paid Users ===")
print(con.execute("""
SELECT plan, COUNT(*) 
FROM subscriptions
WHERE end_date IS NOT NULL
GROUP BY plan
ORDER BY plan
""").fetchdf())

print("\n=== Events Distribution ===")
print(con.execute("""
SELECT event_type, COUNT(*) 
FROM events 
GROUP BY event_type
ORDER BY event_type
""").fetchdf())

con.close()
