import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_USERS = 10000
START_DATE = "-180d"   # 6 months ago
END_DATE = "-30d"      # 1 month ago
DATA_PATH = "data/raw/"

np.random.seed(42)
fake = Faker()

# -----------------------------
# STEP 1: GENERATE USERS
# -----------------------------
users = []

for user_id in range(1, NUM_USERS + 1):
    signup_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)

    users.append({
        "user_id": user_id,
        "signup_date": signup_date,
        "country": np.random.choice(["India", "US", "UK", "Germany"], p=[0.45, 0.25, 0.15, 0.15]),
        "device": np.random.choice(["mobile", "web"], p=[0.6, 0.4]),
        "channel": np.random.choice(["organic", "ads", "referral"], p=[0.5, 0.3, 0.2])
    })

users_df = pd.DataFrame(users)
users_df.to_csv(f"{DATA_PATH}users.csv", index=False)

print("✅ users.csv created")

# -----------------------------
# STEP 2: GENERATE SUBSCRIPTIONS
# -----------------------------
subscriptions = []

for _, user in users_df.iterrows():
    plan = np.random.choice(["free", "basic", "pro"], p=[0.7, 0.2, 0.1])

    start_date = user.signup_date if plan != "free" else None

    # churn probability based on plan
    churn_prob = {"free": 0.6, "basic": 0.35, "pro": 0.15}[plan]

    churned = np.random.rand() < churn_prob

    end_date = None
    if churned and plan != "free":
        end_date = fake.date_between(start_date=start_date, end_date="today")

    subscriptions.append({
        "user_id": user.user_id,
        "plan": plan,
        "start_date": start_date,
        "end_date": end_date
    })

subs_df = pd.DataFrame(subscriptions)
subs_df.to_csv(f"{DATA_PATH}subscriptions.csv", index=False)

print("✅ subscriptions.csv created")

# -----------------------------
# STEP 3: GENERATE EVENTS
# -----------------------------
events = []
event_id = 1

for _, user in users_df.iterrows():
    plan = subs_df.loc[subs_df.user_id == user.user_id, "plan"].values[0]

    # paid users are more active
    avg_events = {"free": 8, "basic": 15, "pro": 25}[plan]
    num_events = np.random.poisson(avg_events)

    start = user.signup_date
    end = pd.to_datetime("today")

    for _ in range(num_events):
        events.append({
            "event_id": event_id,
            "user_id": user.user_id,
            "event_type": np.random.choice(
                ["login", "feature_use", "logout"],
                p=[0.4, 0.4, 0.2]
            ),
            "event_time": fake.date_between(start_date=start, end_date=end)
        })
        event_id += 1

events_df = pd.DataFrame(events)
events_df.to_csv(f"{DATA_PATH}events.csv", index=False)

print("✅ events.csv created")

# -----------------------------
# STEP 4: GENERATE PAYMENTS (FIXED)
# -----------------------------
payments = []
payment_id = 1

for _, sub in subs_df.iterrows():
    if sub.plan in ["basic", "pro"] and pd.notna(sub.start_date):

        amount = 499 if sub.plan == "basic" else 999

        start = pd.to_datetime(sub.start_date)
        end = pd.to_datetime(sub.end_date) if pd.notna(sub.end_date) else pd.to_datetime("today")

        pay_date = start

        while pay_date < end:
            payments.append({
                "payment_id": payment_id,
                "user_id": sub.user_id,
                "amount": amount,
                "payment_date": pay_date.date()
            })
            payment_id += 1
            pay_date += timedelta(days=30)

payments_df = pd.DataFrame(payments)
payments_df.to_csv(f"{DATA_PATH}payments.csv", index=False)

print("✅ payments.csv created")

print("\n🎉 DATASET GENERATION COMPLETED SUCCESSFULLY")
