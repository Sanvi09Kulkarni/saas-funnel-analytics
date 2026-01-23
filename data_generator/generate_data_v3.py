import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

N_USERS = 10000
WEEKS = 12

start_date = datetime(2024, 1, 1)

users = []
events = []
subscriptions = []
payments = []

for i in range(N_USERS):
    user_id = i + 1
    signup = start_date + timedelta(days=random.randint(0, 60))
    
    # ----------- Exploration Phase (Week 0-1) -----------
    exploratory_events = random.randint(1, 10)
    feature_dates = []
    
    for _ in range(exploratory_events):
        event_time = signup + timedelta(days=random.randint(0, 7))
        feature_dates.append(event_time)
        events.append((user_id, event_time, "feature_use"))
    
    # Activation Definition (>=3 uses in first week)
    activated = len(feature_dates) >= 3
    activation_date = min(feature_dates) if activated else None
    
    # ----------- Conversion Logic -----------
    paid = False
    subscription_date = None
    
    if activated:
        if random.random() < 0.12:      # 12% conversion for activated
            paid = True
            subscription_date = activation_date + timedelta(days=random.randint(1, 14))
    else:
        if random.random() < 0.01:      # 1% conversion for non-activated
            paid = True
            subscription_date = signup + timedelta(days=random.randint(7, 30))
    
    if paid:
        subscriptions.append((user_id, subscription_date))
    
    # ----------- Retention + Usage Simulation (Weeks 0-12) -----------
    churned = False
    
    for week in range(WEEKS):
        if churned:
            break
        
        week_start = signup + timedelta(days=7 * week)
        
        # Session Probability
        if paid:
            session_prob = 0.75  # paid are stickier
        elif activated:
            session_prob = 0.55
        else:
            session_prob = 0.25
        
        if random.random() > session_prob:
            # churn event (dropout)
            if random.random() < 0.10:
                churned = True
            continue
        
        # Sessions in the week
        sessions = random.randint(1, 5)
        for _ in range(sessions):
            uses = random.randint(1, 10)
            for __ in range(uses):
                event_time = week_start + timedelta(days=random.randint(0, 6))
                events.append((user_id, event_time, "feature_use"))
    
    # --------- Payments (LTV path) ---------
    if paid:
        # monthly billing for simplicity
        month_count = random.randint(1, 6) if not churned else random.randint(1, 3)
        for m in range(month_count):
            pay_date = subscription_date + timedelta(days=30 * m)
            payments.append((user_id, pay_date, 10.0))  # $10/month

    users.append((user_id, signup, activated, paid))

# Save to CSV
users_df = pd.DataFrame(users, columns=["user_id", "signup_date", "activated", "paid"])
events_df = pd.DataFrame(events, columns=["user_id", "event_time", "event_type"])
subs_df = pd.DataFrame(subscriptions, columns=["user_id", "start_date"])
pay_df = pd.DataFrame(payments, columns=["user_id", "payment_date", "amount"])

users_df.to_csv("../data/raw/users.csv", index=False)
events_df.to_csv("../data/raw/events.csv", index=False)
subs_df.to_csv("../data/raw/subscriptions.csv", index=False)
pay_df.to_csv("../data/raw/payments.csv", index=False)

print("V3 dataset generated successfully!")
