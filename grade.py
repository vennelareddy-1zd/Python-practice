import streamlit as st

st.title("Student Grades")

# Input student info
name = st.text_input("Enter Student Name")
subject1 = st.number_input("Subject1 Marks (0-100)", 0, 100, 0)
subject2 = st.number_input("Subject2 Marks (0-100)", 0, 100, 0)
subject3 = st.number_input("Subject3 Marks (0-100)", 0, 100, 0)

# Calculate average
average = (subject1 + subject2 + subject3) / 3

# Function to determine grade
def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

grade = calculate_grade(average)

# Display results
if name:
    st.write(f"Student: **{name}**")
    st.write(f"Subject1: {subject1}, Subject2: {subject2}, Subject3: {subject3}")
    st.write(f"Average: {average:.2f}")
    st.write(f"Grade: **{grade}**")

