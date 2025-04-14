import streamlit as st
from datetime import datetime, date, time
from utils import load_users, load_data, save_data, calculate_hours

st.set_page_config(page_title="Time Tracker Chatbot", layout="centered")

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Login Page
def login():
    st.title("🔐 Login")
    users = load_users()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid credentials!")

# Admin Dashboard
def admin_view():
    st.title("📊 Admin Dashboard")
    data = load_data()

    if not data:
        st.warning("No data found.")
        return

    for user, user_data in data.items():
        st.subheader(f"👤 {user}")
        total_hours = sum(entry["hours"] for entry in user_data.get("entries", []))
        total_days = len(user_data.get("entries", []))
        average = round(total_hours / total_days, 2) if total_days > 0 else 0

        st.markdown(f"- **Days Present**: {total_days}")
        st.markdown(f"- **Total Hours**: {total_hours}")
        st.markdown(f"- **Average/Day**: {average}")

        with st.expander("View Entries"):
            for entry in user_data.get("entries", []):
                st.write(entry)

# User Dashboard
def user_view():
    st.title("⏱️ Time Tracker")
    username = st.session_state.username
    data = load_data()
    today = date.today()

    selected_date = st.date_input("Select Date", today)
    in_time = st.time_input("Clock In", value=time(9, 0))
    out_time = st.time_input("Clock Out", value=time(17, 0))

    if st.button("Save Entry"):
        worked_hours = calculate_hours(in_time.strftime("%H:%M:%S"), out_time.strftime("%H:%M:%S"))
        entry = {
            "date": str(selected_date),
            "in": in_time.strftime("%H:%M:%S"),
            "out": out_time.strftime("%H:%M:%S"),
            "hours": worked_hours
        }

        if username not in data:
            data[username] = {"entries": []}
        data[username]["entries"].append(entry)
        save_data(data)
        st.success(f"Saved! Hours worked: {worked_hours}")

    # Show Summary
    user_data = data.get(username, {})
    entries = user_data.get("entries", [])
    st.subheader("📊 Monthly Summary")

    total_hours = sum(e["hours"] for e in entries)
    total_days = len(entries)
    avg = round(total_hours / total_days, 2) if total_days else 0

    st.markdown(f"- **Total Days Present**: {total_days}")
    st.markdown(f"- **Total Hours Worked**: {total_hours}")
    st.markdown(f"- **Average Hours per Day**: {avg}")

    with st.expander("📅 View My Entries"):
        for e in entries:
            st.write(e)

# Main App Logic
if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "admin":
        admin_view()
    else:
        user_view()
