# app.py
import streamlit as st
from chatbot import get_bot_response

st.set_page_config(page_title="JD's Chatbot UI", layout="centered")

st.title("💬 JD's Personal Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    # Get response
    response = get_bot_response(user_input)

    # Save to session state
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display conversation
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
