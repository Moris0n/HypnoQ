import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://models:8000/hypno-bot")
print(f"CHATBOT_URL is set to: {CHATBOT_URL}")  # Debugging statement

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        Welcome! This chatbot is here to help you with any questions you might have about cognitive hypnotherapy. 
        If you need more detailed information or aren’t satisfied with the response, you can always contact the therapist directly via email.
        """
    )

    st.header("Example Questions")
    st.markdown("- What is Cognitive Hypnotherapy?")
    st.markdown("- Is hypnosis safe?")
    st.markdown("- Will hypnosis work for me ?")
    st.markdown("- How many session will I need to heal?")
    
st.title("Cognetive Hypnotheraphy Chatbot")
st.info(
    "Feel free to ask me any questions about cognitive hypnotherapy and how it can help you feel more relaxed."
    "I’m here to provide information and support on your journey to well-being. :blue_heart:"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

if prompt := st.chat_input("What do you want to Ask?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"question": prompt}
    print(f"Sending data to {CHATBOT_URL}: {data}")  # Debugging statement


    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)    
        print(f"Response status code: {response.status_code}")  # Debugging statement
        print(f"Response content: {response.content}")  # Debugging statement

        if response.status_code == 200:
            output_text = response.json().get("output", "No output key in response")
        else:
            output_text = f"An error occurred: {response.status_code}\n{response.content.decode()}"


    st.chat_message("assistant").markdown(output_text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
        }
    )