import streamlit as st
import pandas as pd

# Inject custom CSS for styling and animations
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            font-family: 'Arial', sans-serif;
            color: white;
        }

        .stButton>button {
            background-color: #0072ff;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #00c6ff;
            cursor: pointer;
        }

        h1, h2, h3 {
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }

        table {
            width: 100%;
            margin-top: 30px;
            border-collapse: collapse;
            animation: fadeIn 2s ease-in-out;
        }

        th, td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        th {
            background-color: #0072ff;
            color: white;
        }

        td {
            background-color: #ffffff;
            color: #333;
        }

        .status {
            font-weight: bold;
            color: #4CAF50;
        }

        .status.not-done {
            color: #f44336;
        }

        /* Animation */
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)


def daywise_timetable():
    # Define the time slots for day-wise timetable
    time_slots = [
        ("8:00 AM - 9:30 AM", "", "Not Done"),
        ("9:45 AM - 10:45 AM", "", "Not Done"),
        ("11:30 AM - 1:00 PM", "", "Not Done"),
        ("2:00 PM - 4:00 PM", "", "Not Done"),
        ("4:30 PM - 5:30 PM", "", "Not Done"),
        ("5:30 PM - 7:00 PM", "", "Not Done"),
        ("8:00 PM - 10:00 PM", "", "Not Done"),
        ("10:30 PM - 12:00 AM", "", "Not Done")
    ]

    # Create a DataFrame for day-wise timetable
    daywise_df = pd.DataFrame(time_slots, columns=["Time", "Subject(s)", "Status"])

    # Allow user to fill in subjects for each time slot and select the status (Done/Not Done)
    for i in range(len(daywise_df)):
        daywise_df.at[i, "Subject(s)"] = st.text_input(f"Time Slot {daywise_df.at[i, 'Time']}",
                                                        daywise_df.at[i, "Subject(s)"])
        daywise_df.at[i, "Status"] = st.selectbox(f"Did you complete {daywise_df.at[i, 'Subject(s)']}?",
                                                  ["Not Done", "Done"], key=f"status_day_{i}")

    return daywise_df


def weekwise_timetable():
    # Define the number of weeks (from Week 1 to Week 104, approx 2 years)
    weeks = list(range(1, 105))  # Weeks from 1 to 104

    # Create a DataFrame for Week-wise timetable with empty subjects
    weekwise_df = pd.DataFrame({
        'Week Number': weeks,
        'Subjects': [''] * len(weeks),  # Empty subject field initially
        'Status': [''] * len(weeks)  # Status field for completion
    })

    # Allow user to input multiple subjects for each week and mark completion status
    subjects_for_weeks = []  # List to store subjects for each week
    
    for i in range(len(weekwise_df)):
        week = weekwise_df.at[i, 'Week Number']
        st.subheader(f"Week {week} Subjects")
        
        # Allow user to add multiple subjects for each week
        subjects_input = st.text_area(f"Enter subjects for Week {week} (comma-separated):", "")
        subjects = [subject.strip() for subject in subjects_input.split(',') if subject.strip()]  # Split by commas
        
        if subjects:
            for j, subject in enumerate(subjects):
                st.write(f"Subject {j + 1}: {subject}")
                status = st.selectbox(f"Did you complete {subject}?", ["Not Completed", "Completed"], key=f"status_week_{week}_{j}")
                subjects_for_weeks.append((week, subject, status))

        weekwise_df.at[i, 'Subjects'] = ", ".join(subjects)
        weekwise_df.at[i, 'Status'] = ", ".join([status for _, _, status in subjects_for_weeks if _ == week])

    return weekwise_df




def main():
    st.title("Time Table Planner")

    # Sidebar for displaying the update table
    st.sidebar.title("Update Table")

    # Call daywise timetable
    st.subheader("Daywise Time Table")
    daywise_df = daywise_timetable()

    # Call weekwise timetable
    st.subheader("Weekwise Time Table")
    weekwise_df = weekwise_timetable()

    # Show updated tables on the sidebar
    with st.sidebar:
        st.subheader("Update Status Table")
        st.write("### Daywise Timetable Updates")
        st.write(daywise_df)

        st.write("### Weekwise Timetable Updates")
        st.write(weekwise_df)

if __name__ == "__main__":
    main()
