# timetracker.py
import streamlit as st
from datetime import datetime

# Dummy auth for now (replace later with Firebase)
USERS = {
    "admin@example.com": {"role": "admin", "password": "admin123"},
    "angajat1@example.com": {"role": "employee", "password": "pass123"},
}

# Dummy employee list
EMPLOYEES = [
    {"name": "Emma Johnson", "phone": "0123 456 789"},
    {"name": "Michael Smith", "phone": "0123 456 789"},
    {"name": "Olivia Brown", "phone": "0123 456 789"},
    {"name": "Sophia Wilson", "phone": "0123 456 789"},
    {"name": "James Miller", "phone": "0123 456 789"},
    {"name": "Isabella Anderson", "phone": "0123 456 789"},
]

# Session state login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# Login page
if not st.session_state.logged_in:
    st.set_page_config(page_title="Time Tracker", layout="wide")
    st.title("Time Tracker Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = USERS.get(email)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = {"email": email, "role": user["role"]}
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
else:
    user = st.session_state.user
    st.set_page_config(page_title="Time Tracker Dashboard", layout="wide")
    st.sidebar.title("Time Tracker")
    st.sidebar.write(f"Logged in as {user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    if user['role'] == 'admin':
        menu = st.sidebar.radio("Navigation", ["Employees", "Time Tracking", "Reports"])

        if menu == "Employees":
            st.title("Employees")
            cols = st.columns([3, 1])
            with cols[0]:
                st.subheader("Employee")
                for emp in EMPLOYEES:
                    st.write(f"{emp['name']} - {emp['phone']}")

            with cols[1]:
                st.subheader("Add Employee")
                new_name = st.text_input("Name")
                new_phone = st.text_input("Phone")
                if st.button("Add Employee"):
                    EMPLOYEES.append({"name": new_name, "phone": new_phone})
                    st.success("Employee added.")
                    st.experimental_rerun()

        elif menu == "Time Tracking":
            st.title("Time Tracking")
            st.subheader("Save")
            employee_names = [e['name'] for e in EMPLOYEES]
            selected_employee = st.selectbox("Select Employee", employee_names)
            date = st.date_input("Date", datetime.today())
            location = st.selectbox("Location", ["Location A", "Location B", "Location C"])
            if st.button("Save"):
                st.success(f"Saved time tracking for {selected_employee} at {location} on {date}.")

            st.subheader("Time Tracking Summary")
            st.write("**Weekly**")
            st.write("Emma Johnson - 40")
            st.write("Location A - 60")
            st.write("Total - 100")

        elif menu == "Reports":
            st.title("Reports")
            st.subheader("Weekly")
            st.write("Emma Johnson")
            st.table({
                "Date": ["03/18/2024", "03/18/2024", "03/17/2024"],
                "Hours": [8, 60, 100],
                "Location": ["Location A", "Location A", "Total"]
            })

    elif user['role'] == 'employee':
        st.title("Employee Dashboard")
        st.write("Here you will see your assigned shifts and confirm location.")
