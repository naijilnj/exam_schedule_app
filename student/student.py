import streamlit as st
import pandas as pd
from pymongo import MongoClient
import shared

# Initialize MongoDB client
client = MongoClient("mongodb+srv://naijilaji:8FS9IVijl1HjtYMZ@scheduleapp.s8rln09.mongodb.net/")  # Update with your MongoDB URI

# Select the database
db = client["students_logindetails"]  # Replace "your_database_name" with your actual database name

# Select the collection
collection = db["students"]  # Assuming you have a collection named "students" to store student data

# List of departments
DEPARTMENTS = ["IT", "CS", "BCA", "BBA", "BMS"]

# Function for student authentication
def student_authentication(email, department):
    return email.endswith("@somaiya.edu") and department in DEPARTMENTS

# Function to insert email and department into MongoDB collection
def insert_student_data(email, department):
    try:
        collection.insert_one({"email": email, "department": department})
        return True
    except Exception as e:
        print("Error inserting student data into MongoDB:", e)
        return False

# Student page
def student_page():
    st.title("Check Your Upcoming Exams")

    # Check if the user has already authenticated
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        st.write("Department:", st.session_state.department)  # Display department name
        student_view_schedule()
        return

    # Initialize session state variables if not already initialized
    if 'email' not in st.session_state:
        st.session_state.email = ""
    if 'department' not in st.session_state:
        st.session_state.department = DEPARTMENTS[0]  # Set initial department to the first in the list

    # Student authentication
    st.header("Student Authentication")
    email = st.text_input("Enter Your Email", value=st.session_state.email)
    department = st.selectbox("Select Your Department", DEPARTMENTS, index=DEPARTMENTS.index(st.session_state.department))

    # Check if the "Login" button is clicked
    if st.button("Login"):
        if student_authentication(email, department):
            if insert_student_data(email, department):
                shared.set_authenticated(email, department)
                st.success("Authentication Successful")
            else:
                st.error("Error occurred during authentication")
    
    # Hide the authentication section if authentication is successful
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        st.write("Department:", st.session_state.department)  # Display department name
        student_view_schedule()

# Student View Schedule Page
def student_view_schedule():
    st.title("Upcoming Exams")
    schedule_data = shared.load_schedule_data()
    if schedule_data:
        st.write("Exam Schedule")
        filtered_schedule = []
        for entry in schedule_data:
            if entry.get('department') == st.session_state.department:
                filtered_schedule.append(entry)
        if filtered_schedule:
            df = pd.DataFrame(filtered_schedule)
            df = df[['name', 'date']]  # Exclude department from display
            st.table(df)
        else:
            st.write("No schedule available for your department.")
    else:
        st.write("No schedule available.")


def main():
    student_page()

if __name__ == "__main__":
    main()
