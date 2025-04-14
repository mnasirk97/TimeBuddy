import json
from datetime import datetime

# Load login users
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

# Load time entries
def load_data():
    with open("database.json", "r") as f:
        return json.load(f)

# Save time entries
def save_data(all_data):
    with open("database.json", "w") as f:
        json.dump(all_data, f, indent=4)

# Calculate worked hours
def calculate_hours(in_time, out_time):
    in_dt = datetime.strptime(in_time, "%H:%M:%S")
    out_dt = datetime.strptime(out_time, "%H:%M:%S")
    duration = out_dt - in_dt
    return round(duration.total_seconds() / 3600, 2)
