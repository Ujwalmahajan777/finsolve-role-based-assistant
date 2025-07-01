import streamlit as st
import requests

# Set up the page
st.set_page_config(page_title="FinSolve Assistant", layout="centered")
st.title("FinSolve Assistant")

# Keep chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Select role
role = st.selectbox("Select your role:", ["finance", "hr", "marketing", "tech", "compliance", "general", "c-level"])

# Input
question = st.text_input("Enter your question:")

# Submit
if st.button("Submit") and question:
    # Exit check
    if question.strip().lower() == "quit":
        st.session_state.messages.append(("You", question))
        st.session_state.messages.append(("Assistent", "👋 Thank you for using FinSolve Assistant."))
    else:
        st.session_state.messages.append(("You", question))
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={"role": role, "question": question}
        )

        if response.status_code == 200:
            answer = response.json().get("answer", "")
        else:
            answer = "Something went wrong. Please try again."

        st.session_state.messages.append(("Assistent", answer))

# Display history
st.markdown("---")
for sender, msg in reversed(st.session_state.messages):
    st.write(f"**{sender}:** {msg}")
