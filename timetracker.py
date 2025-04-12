import streamlit as st
from datetime import datetime

# -------------- Fake Auth and Dummy Data ----------------
USERS = {
    "admin@example.com": {"role": "admin", "password": "admin123"},
    "angajat1@example.com": {"role": "employee", "password": "pass123"},
}

EMPLOYEES = [
    {"name": "Emma Johnson", "phone": "0123 456 789"},
    {"name": "Michael Smith", "phone": "0123 456 789"},
    {"name": "Olivia Brown", "phone": "0123 456 789"},
    {"name": "Sophia Wilson", "phone": "0123 456 789"},
    {"name": "James Miller", "phone": "0123 456 789"},
    {"name": "Isabella Anderson", "phone": "0123 456 789"},
]

LOCATIONS = ["Location A", "Location B", "Location C"]

# -------------- Session Setup ----------------
st.set_page_config(page_title="Time Tracker", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# -------------- Login Page ----------------
if not st.session_state.logged_in:
    st.title("💼 Time Tracker Login")
    with st.form("login_form"):
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        submitted = st.form_submit_button("🔓 Login")
        if submitted:
            user = USERS.get(email)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = {"email": email, "role": user["role"]}
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Try again.")

# -------------- Logged In Interface ----------------
else:
    user = st.session_state.user
    st.sidebar.title("🕒 Time Tracker")
    st.sidebar.caption(f"Logged in as: **{user['email']}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

    if user["role"] == "admin":
        menu = st.sidebar.radio("📂 Menu", ["👥 Employees", "📅 Time Tracking", "📈 Reports"])

        # --- EMPLOYEES PAGE ---
        if menu == "👥 Employees":
            st.title("👥 Employees Management")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("Current Employees")
                for emp in EMPLOYEES:
                    st.markdown(f"🧑‍💼 **{emp['name']}** – 📞 {emp['phone']}")

            with col2:
                st.subheader("➕ Add Employee")
                new_name = st.text_input("Name")
                new_phone = st.text_input("Phone")
                if st.button("Add"):
                    EMPLOYEES.append({"name": new_name, "phone": new_phone})
                    st.success(f"Added {new_name}")
                    st.rerun()

        # --- TIME TRACKING PAGE ---
        elif menu == "📅 Time Tracking":
            st.title("📅 Assign Time to Employees")

            employee_names = [e["name"] for e in EMPLOYEES]
            selected_employee = st.selectbox("👤 Select Employee", employee_names)
            date = st.date_input("📆 Date", datetime.today())
            location = st.selectbox("📍 Location", LOCATIONS)
            hours = st.number_input("⏱️ Hours Worked", min_value=0.0, max_value=24.0, step=0.5)

            if st.button("💾 Save Entry"):
                st.success(f"Saved: {selected_employee} worked {hours}h at {location} on {date.strftime('%Y-%m-%d')}")

            st.markdown("---")
            st.markdown("### 🧾 Summary")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Employee", selected_employee)
            col2.metric("Location", location)
            col3.metric("Hours", f"{hours}h")
            col4.metric("Date", date.strftime("%d %b %Y"))

            st.markdown("### 📋 Preview Table")
            st.dataframe({
                "Date": [date.strftime("%Y-%m-%d")],
                "Employee": [selected_employee],
                "Hours": [hours],
                "Location": [location],
            }, use_container_width=True)

        # --- REPORTS PAGE ---
        elif menu == "📈 Reports":
            st.title("📈 Weekly / Monthly Reports")
            st.write("Placeholder report view (static data for now)")

            st.table({
                "Date": ["2024-03-18", "2024-03-18", "2024-03-17"],
                "Employee": ["Emma Johnson", "Emma Johnson", "Emma Johnson"],
                "Hours": [8, 6, 10],
                "Location": ["Location A", "Location A", "Total"]
            })

    # === EMPLOYEE DASHBOARD ===
    elif user["role"] == "employee":
        st.title("👤 Employee Dashboard")
        st.info("Here you will see your assigned location and confirm attendance. Coming soon.")
