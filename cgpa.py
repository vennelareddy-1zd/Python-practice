import streamlit as st

st.title("CGPA Calculator")

# Input student info
name = st.text_input("Enter Student Name")

# Number of subjects
num_subjects = st.number_input("Enter Number of Subjects", min_value=1, max_value=20, step=1)

# Initialize lists to store marks and credits
marks_list = []
credits_list = []

# Dynamically create input fields for each subject
for i in range(1, num_subjects + 1):
    st.subheader(f"Subject {i}")
    marks = st.number_input(f"Marks for Subject {i} (0-100)", 0, 100, 0, key=f"marks{i}")
    credits = st.number_input(f"Credits for Subject {i}", 1, 10, 3, key=f"credits{i}")
    marks_list.append(marks)
    credits_list.append(credits)

# Function to convert marks to grade points
def marks_to_gp(marks):
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    else:
        return 0

# Calculate grade points for each subject
gp_list = [marks_to_gp(m) for m in marks_list]

# Calculate CGPA
total_credits = sum(credits_list)
weighted_sum = sum([gp * cr for gp, cr in zip(gp_list, credits_list)])
cgpa = weighted_sum / total_credits

# Display results
if name:
    st.write(f"Student: **{name}**")
    for i in range(num_subjects):
        st.write(f"Subject {i+1}: Marks = {marks_list[i]}, Credits = {credits_list[i]}, GP = {gp_list[i]}")
    st.write(f"**CGPA: {cgpa:.2f}**")
