import streamlit as st
import yaml, os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from google.api_core.exceptions import InvalidArgument, PermissionDenied, Unauthenticated


@st.cache_data
def is_valid_apikey(api_key):
    llm = get_llm(api_key)
    try:
        response = llm.invoke("Hello")
        print(response)
        return True
    
    except (InvalidArgument, PermissionDenied, Unauthenticated):
        return False
    
    except Exception as e:
        raise Exception(e)
    
@st.cache_data
def get_llm(api_key):
    model = utils.params['google_model']
    return GoogleGenerativeAI(model=model, api_key=api_key)


def initialize_chat_utils(api_key):
    if 'chat_utils_instance' not in st.session_state:
        st.session_state['chat_utils_instance'] = ChatUtils(api_key)
    else:
        pass

    return st.session_state['chat_utils_instance']


class Utils:
    def __init__(self):
        self.params_filepath = os.path.join(os.getcwd(), "params.yaml")
        self.params = self.load_params()

    def load_params(self):
        with open(self.params_filepath, 'r') as file:
            params = yaml.safe_load(file)

        return params



class ChatUtils:
    def __init__(self, api_key):
        self.set_things_up(api_key)

    def set_things_up(self, api_key):
        self.api_key = api_key
        self.messages = self.set_messages_as_list_in_session()
        self.prepare_messages()
        self.chat_model = self.get_chat_model()

    def set_messages_as_list_in_session(self):
        if 'messages' not in st.session_state:
            st.session_state['messages'] = []

    def prepare_messages(self):
        self.system_message = utils.params['system_message']
        self.add_message_to_messages(self.system_message, "system")

    def get_chat_model(self):
        chat_model = ChatGoogleGenerativeAI(model = utils.params['google_model'])
        return chat_model

    def process_user_message(self, message):
        self.add_message_to_messages(message, "human")
        
        response = self.chat_model.invoke(st.session_state['messages'])
        self.add_message_to_messages(response.content, "ai")
        return st.session_state['messages']

    def add_message_to_messages(self, message: str, role: str):
        message = (role, message)
        st.session_state['messages'].append(message)





utils = Utils()