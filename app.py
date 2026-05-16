import streamlit as st
import pickle
import re

# LOAD MODEL & VECTORIZER
model = pickle.load(open("model.pkl", "rb"))

vectorizer = pickle.load(
    open("vectorizer.pkl", "rb")
)

# PAGE TITLE
st.title("HR AI Ticket Routing System")

st.write(
    "AI-powered HR ticket classification and information extraction"
)

# USER INPUT
ticket = st.text_area(
    "Enter Employee Ticket"
)

# ANALYZE BUTTON
if st.button("Analyze"):

    # VECTORIZE INPUT
    vectorized = vectorizer.transform([ticket])

    # ML PREDICTION
    prediction = model.predict(vectorized)[0]

    text_lower = ticket.lower()

    # RULE-BASED OVERRIDES
    if "leave" in text_lower:
        prediction = "Update Leave"

    elif "week off" in text_lower:
        prediction = "Shift Mapping / Week Off"

    elif "attendance" in text_lower:
        prediction = "Time & Attendance Questions"

    elif "punch" in text_lower:
        prediction = "Working Time Corrections"

    # DATE EXTRACTION
    date_pattern = r'''
    \b(
        \d{1,2}[/-]\d{1,2}[/-]\d{2,4} |
        \d{1,2}(st|nd|rd|th)?\s
        (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|
        January|February|March|April|May|June|July|August|
        September|October|November|December)
    )
    \b
    '''

    date_match = re.search(
        date_pattern,
        ticket,
        re.IGNORECASE | re.VERBOSE
    )

    extracted_date = (
        date_match.group()
        if date_match
        else "Not Found"
    )

    # LEAVE TYPE EXTRACTION
    leave_types = [
        "earned leave",
        "sick leave",
        "casual leave",
        "maternity leave"
    ]

    detected_leave = "Not Found"

    for leave in leave_types:
        if leave in text_lower:
            detected_leave = leave.title()
            break

    # SHIFT EXTRACTION
    shift_keywords = [
        "morning shift",
        "night shift",
        "general shift",
        "a shift",
        "b shift",
        "c shift"
    ]

    detected_shift = "Not Found"

    for shift in shift_keywords:
        if shift in text_lower:
            detected_shift = shift.title()
            break

    # WEEK OFF DAYS EXTRACTION
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    detected_days = []

    for day in days:
        if day in text_lower:
            detected_days.append(day.title())

    # DISPLAY RESULTS
    st.subheader("Extracted Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Category", prediction)

    with col2:
        st.metric("Date", extracted_date)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Leave Type", detected_leave)

    with col4:
        st.metric("Shift", detected_shift)

    st.write("### Week Off Days")

    if detected_days:
        st.write(", ".join(detected_days))
    else:
        st.write("Not Found")
