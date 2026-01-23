import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

N_USERS = 10000

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 1)

users = []
events = []
subscriptions = []

for i in range(N_USERS):
    user_id = i + 1
    signup = fake.date_between(start_date=start_date, end_date=end_date)
    
    # Exploration Phase (Day 0–7)
    exploratory_events = random.randint(1, 10)
    
    feature_dates = []
    for _ in range(exploratory_events):
        event_time = signup + timedelta(days=random.randint(0, 7))
        events.append((user_id, event_time, "feature_use"))
        feature_dates.append(event_time)
    
    activated = False
    if len(feature_dates) >= 3:
        activated = True
        activation_date = min(feature_dates)
    else:
        activation_date = None
    
    # Conversion Phase (Activation → Paid)
    if activated:
        if random.random() < 0.12:   # 12% conversion
            paid_date = activation_date + timedelta(days=random.randint(1, 14))
            subscriptions.append((user_id, paid_date))
    else:
        # Rare non-activated conversions
        if random.random() < 0.01:
            paid_date = signup + timedelta(days=random.randint(7, 30))
            subscriptions.append((user_id, paid_date))
    
    users.append((user_id, signup, activated))

# ---- Convert to dataframes ----
users_df = pd.DataFrame(users, columns=["user_id", "signup_date", "activated"])
events_df = pd.DataFrame(events, columns=["user_id", "event_time", "event_type"])
subs_df = pd.DataFrame(subscriptions, columns=["user_id", "start_date"])

# Save
users_df.to_csv("../data/raw/users.csv", index=False)
events_df.to_csv("../data/raw/events.csv", index=False)
subs_df.to_csv("../data/raw/subscriptions.csv", index=False)

print("Generated V2 dataset successfully!")
