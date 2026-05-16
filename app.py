import streamlit as st
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

vectorizer = pickle.load(
    open("vectorizer.pkl", "rb")
)

st.title("HR AI Ticket Routing System")

ticket = st.text_area(
    "Enter Employee Ticket"
)

if st.button("Analyze"):

    vectorized = vectorizer.transform([ticket])

    prediction = model.predict(vectorized)

    st.write("Category:", prediction[0])