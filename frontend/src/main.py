import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://models:8000/hypno-bot")
FEEDBACK_URL = os.getenv("FEEDBACK_URL", "http://models:8000/feedback")

# Sidebar content
with st.sidebar:
    st.header("About")
    st.markdown("""
    Welcome! This chatbot is here to help you with any questions you might have about cognitive hypnotherapy. 
    If you need more detailed information or aren’t satisfied with the response, you can always contact the therapist directly via email.
    """)

    st.header("Example Questions")
    st.markdown("- What is Cognitive Hypnotherapy?")
    st.markdown("- Is hypnosis safe?")
    st.markdown("- Will hypnosis work for me?")
    st.markdown("- How many sessions will I need to improve?")

st.title("Cognitive Hypnotherapy Chatbot")
st.info(
    "Feel free to ask me any questions about cognitive hypnotherapy and how it can help you feel more relaxed."
    "I’m here to provide information and support on your journey to well-being. :blue_heart:"
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message:
            st.markdown(message["output"])

# User input
if prompt := st.chat_input("What do you want to ask?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"question": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json().get("output", "No output key in response")
        else:
            output_text = f"An error occurred: {response.status_code}\n{response.content.decode()}"

    st.chat_message("assistant").markdown(output_text)

    st.session_state.messages.append(
        {"role": "assistant", "output": output_text}
    )

    # Add feedback buttons after the chatbot response
    st.write("Was this answer helpful?")
    if st.button("👍 Yes"):
        feedback_data = {"question": prompt, "helpful": True}
        feedback_response = requests.post(FEEDBACK_URL, json=feedback_data)
        st.success(feedback_response.json().get("message", "Thank you for your feedback!"))

    if st.button("👎 No"):
        feedback_data = {"question": prompt, "helpful": False}
        feedback_response = requests.post(FEEDBACK_URL, json=feedback_data)
        st.warning(feedback_response.json().get("message", "Sorry, we'll review the question."))
