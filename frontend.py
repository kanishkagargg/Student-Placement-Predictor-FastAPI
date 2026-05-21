import streamlit as st
import requests


# API_URL = "http://34.226.152.222:8000/predict" 
API_URL = "http://127.0.0.1:8000/predict" 

st.title("Student Placement Predictor")
st.markdown("Enter your details below:")

# Input fields
previous_score = st.number_input("Previous score of the student", min_value=0, max_value=100, value=50)
study_hours = st.number_input("Study hours per day", min_value=0, max_value=24, value=4)
attendance = st.number_input("Attendance (%)", min_value=0, max_value=100, value=80)
sleep_hours = st.number_input("Sleep hours per day", min_value=0, max_value=24, value=8)
assignments_completed = st.number_input("Assignments completed", min_value=0, value=5)
internet_usage = st.number_input("Internet usage hours per day", min_value=0, max_value=24, value=2)
exam_score = st.number_input("Exam score", min_value=0, max_value=100, value=60)

if st.button("Predict Performance Category"):
    input_data = {
        "previous_score": previous_score,
        "study_hours": study_hours,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "assignments_completed": assignments_completed,
        "internet_usage": internet_usage,
        "exam_score": exam_score
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Placement Category: **{prediction['predicted_category']}**")
            st.write("🔍 Confidence:", prediction["confidence"])
            st.write("📊 Class Probabilities:")
            st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
