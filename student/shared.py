# shared.py
import streamlit as st
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient("mongodb+srv://naijilaji:8FS9IVijl1HjtYMZ@scheduleapp.s8rln09.mongodb.net/")  # Update with your MongoDB URI

# Select the database
db = client["students_logindetails"]  # Replace "students_logindetails" with your actual database name

# Select the collection
collection = db["exam_schedule"]  # Replace "exam_schedule" with your actual collection name

# Function to save schedule data to MongoDB
def save_schedule_data(exam_name, exam_date, department):
    try:
        # Insert the schedule data into the collection
        collection.insert_one({
            "name": exam_name,
            "date": str(exam_date),
            "department": department
        })
    except Exception as e:
        print("Error saving schedule data to MongoDB:", e)

# Function to load schedule data from MongoDB
def load_schedule_data():
    try:
        data = list(collection.find())
        return data
    except Exception as e:
        print("Error loading schedule data from MongoDB:", e)
        return []

# List of departments
DEPARTMENTS = ["IT", "CS", "BCA", "BBA", "BMS"]

# Function to set authenticated status and store user details
def set_authenticated(email, department):
    # Here you can implement the logic to set authenticated status
    # and store user details, such as in a session state or database
    # For example, you can use session state like this:
    st.session_state.authenticated = True
    st.session_state.email = email
    st.session_state.department = department

