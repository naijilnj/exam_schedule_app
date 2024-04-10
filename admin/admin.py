import streamlit as st
import pandas as pd
import shared

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# Function for admin authentication
def admin_authentication(username, password):
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD

# Function to view schedule
def view_schedule():
    schedule_data = shared.load_schedule_data()
    if schedule_data:
        st.write("Uploaded Schedule:")
        df = pd.DataFrame(schedule_data)
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to datetime
        df['date'] = df['date'].dt.strftime('%d/%m/%Y')  # Format date as Day/Month/Year
        st.table(df[::-1].reset_index(drop=True))  # Display DataFrame as a table
    else:
        st.write("No schedule uploaded yet.")

# Admin page
def admin_page():
    st.title("Admin Page")

    # Admin authentication
    st.header("Admin Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if admin_authentication(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
            admin_main()
        else:
            st.error("Invalid username or password")

# Admin dashboard
def admin_main():
    st.title("Admin Dashboard")
    st.sidebar.title("Options")
    option = st.sidebar.radio("Select Option", ("Upload Schedule", "View Schedule"))

    if option == "Upload Schedule":
        exam_name = st.text_input("Name of the Exam")
        exam_date = st.date_input("Date of the Exam")
        department = st.selectbox("Select Department", shared.DEPARTMENTS)
        semester = st.selectbox("Select Semester", ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6"])
        if st.button("Upload"):
            shared.save_schedule_data(exam_name, exam_date, department, semester)  # Call save_schedule_data function
            st.success("Schedule Uploaded Successfully!")
            view_schedule()  # View updated schedule after upload

    elif option == "View Schedule":
        view_schedule()

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        admin_main()
    else:
        admin_page()

if __name__ == "__main__":
    main()
