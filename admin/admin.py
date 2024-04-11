import streamlit as st
from shared import connect_to_mongodb
from datetime import datetime
import pandas as pd

def upload_schedule(collection):
    st.title("Upload Exam Schedule")

    exam_name = st.text_input("Exam Name")
    exam_date = st.date_input("Select Date of Exam", min_value=datetime.today())
    
    # Convert date to datetime
    exam_date = datetime.combine(exam_date, datetime.min.time())

    # Dropdown menu for department selection
    departments = ["IT", "CS", "BCA", "BBA", "BMS"]
    department = st.selectbox("Department", departments)

    # Dropdown menu for semester selection
    semesters = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5"]
    semester = st.selectbox("Semester", semesters)

    if st.button("Upload"):
        schedule_data = {
            "exam_name": exam_name,
            "exam_date": exam_date,
            "department": department,
            "semester": semester
        }
        collection.insert_one(schedule_data)
        st.success("Schedule uploaded successfully!")

def view_recent_schedule(collection):
    st.sidebar.title("Admin Menu")
    page = st.sidebar.radio("Navigation", ["Upload Schedule", "View Schedule"])
    
    if page == "Upload Schedule":
        upload_schedule(collection)
    elif page == "View Schedule":
        st.title("View Exam Schedule")
        schedule_data = collection.find({}, {"_id": 0}).sort("exam_date", -1)
        df = pd.DataFrame(list(schedule_data))
        
        # Format the date column to remove time
        df['exam_date'] = df['exam_date'].dt.strftime('%Y-%m-%d')
        
        st.table(df)

def main():
    st.set_page_config(layout="wide")
    collection = connect_to_mongodb()  # Get MongoDB collection

    # Sidebar for navigation and recent schedule view
    view_recent_schedule(collection)

if __name__ == "__main__":
    main()
