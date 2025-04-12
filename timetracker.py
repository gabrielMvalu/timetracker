# timetracker.py (clean, dark-themed, minimal UI)
import streamlit as st
from datetime import datetime

# Dummy auth
USERS = {
    "admin@example.com": {"role": "admin", "password": "admin123"},
    "angajat1@example.com": {"role": "employee", "password": "pass123"},
}

# Dummy data
EMPLOYEES = [
    {"name": "Emma Johnson", "phone": "0123 456 789"},
    {"name": "Michael Smith", "phone": "0123 456 789"},
    {"name": "Olivia Brown", "phone": "0123 456 789"},
    {"name": "Sophia Wilson", "phone": "0123 456 789"},
    {"name": "James Miller", "phone": "0123 456 789"},
    {"name": "Isabella Anderson", "phone": "0123 456 789"},
]

LOCATIONS = ["Location A", "Location B", "Location C"]

st.set_page_config(page_title="Time Tracker", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.markdown("""
        <style>
        .block-container { padding-top: 5vh; max-width: 600px; }
        </style>
    """, unsafe_allow_html=True)
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            user = USERS.get(email)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = {"email": email, "role": user["role"]}
                st.rerun()
            else:
                st.error("Invalid credentials")
else:
    user = st.session_state.user
    st.sidebar.title("Time Tracker")
    st.sidebar.caption(f"Logged in as: {user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    if user['role'] == 'admin':
        menu = st.sidebar.radio("Navigation", ["Employees", "Time Tracking", "Reports"])

        if menu == "Employees":
            st.title("Employees")
            col_left, col_right = st.columns([3, 1])

            with col_left:
                st.subheader("Employee List")
                for i, emp in enumerate(EMPLOYEES):
                    cols = st.columns([3, 2, 1])
                    cols[0].markdown(f"**{emp['name']}**")
                    cols[1].markdown(emp['phone'])
                    if cols[2].button("Delete", key=f"del_{i}"):
                        EMPLOYEES.pop(i)
                        st.rerun()

            with col_right:
                st.subheader("Add New")
                name = st.text_input("Full Name")
                phone = st.text_input("Phone Number")
                if st.button("Add Employee") and name:
                    EMPLOYEES.append({"name": name, "phone": phone})
                    st.success("Employee added.")
                    st.rerun()

        elif menu == "Time Tracking":
            st.title("Time Tracking")
            employee_names = [e["name"] for e in EMPLOYEES]
            selected_employee = st.selectbox("Select Employee", employee_names)
            date = st.date_input("Date", datetime.today())
            location = st.selectbox("Location", LOCATIONS)
            hours = st.number_input("Hours Worked", min_value=0.0, max_value=24.0, step=0.5)

            if st.button("Save Entry"):
                st.success(f"Saved time tracking for {selected_employee}")

            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown("### Employee")
            col1.markdown(f"**{selected_employee}**")

            col2.markdown("### Location")
            col2.markdown(f"**{location}**")

            col3.markdown("### Hours")
            col3.markdown(f"**{hours}h**")

            col4.markdown("### Date")
            col4.markdown(f"**{date.strftime('%d %b %Y')}**")

        elif menu == "Reports":
            st.title("Reports")
            st.markdown("#### Weekly")
            st.dataframe({
                "Date": ["2024-03-18", "2024-03-18", "2024-03-17"],
                "Employee": ["Emma Johnson", "Emma Johnson", "Emma Johnson"],
                "Hours": [8, 6, 10],
                "Location": ["Location A", "Location A", "Total"]
            }, use_container_width=True)

    elif user['role'] == 'employee':
        st.title("Employee Dashboard")
        st.info("Here you will see your assigned location and confirm attendance.")
