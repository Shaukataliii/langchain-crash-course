import streamlit as st
from utils import is_valid_apikey, initialize_chat_utils, ChatUtils


st.set_page_config("Chatbot", page_icon=":desktop_computer:")
st.header("MS Office Chatbot :desktop_computer:")


with st.sidebar:
    api_key = st.text_input("Enter your Google API key:")

message = st.chat_input("Enter your message here.")

if message:
    if not is_valid_apikey(api_key):
        st.error("Invalid API key.")

    chat_utils = initialize_chat_utils(api_key)
    all_messages = chat_utils.process_user_message(message)
    

    # printing messages
    for role, message in all_messages:
        if role == "human":
            with st.chat_message("human"):
                st.write(message)

        if role == "ai":
            with st.chat_message("assistant"):
                st.write(message)

        else:
            pass