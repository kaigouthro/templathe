import os
import streamlit as st

from defaults import DefaultSettings
from constants import *
from utils import *
from state import PersistentState

from streamlit.runtime.state.session_state_proxy import SessionStateProxy

STATE  = PersistentState(SessionStateProxy, os.path.join(os.getcwd(),'session_state.pkl')).session_state_proxy()


class StateInitializer:
    def __init__(self, state: SessionStateProxy):
        if hasattr(state, 'settings') and hasattr(state, 'profiles') and hasattr(state, 'skills'  ):
            return
        else:
            DefaultSettings(state)
        set_to_state(state, "acelang", "python")
        set_to_state(state, "acetheme", "tomorrow_night")
        self.key_check(state)
        get_models(state)
        st.sidebar.selectbox("Completion Engine",state.models,key="model")

    def key_check(self, state):
        # check if in dev mode to bypass re-entering key
        params = st.experimental_get_query_params()
        state["dev"] =  "None" if "dev" not in params else params["dev"][0]
        dev_input    =  state.get("dev", False)
        if dev_input == st.secrets.creds.password:
            state.api_key = st.secrets.creds.key
        else:
            set_to_state(state, "api_key", None)

        if is_api_key_valid(state.api_key, state) is not True:
            st.sidebar.text_input("Please enter OpenAI Key",key = 'api_key')
            st.stop()


StateInitializer(STATE)


class Handle:
    """Handle class for a langchain tool usable by a GPT-chat agent"""

    def __init__(self, name: str, description: str, tool = None, template = None):
        self.name        : str = name
        self.description : str = description
        self.template          = template
        self.tool              = tool
        self.input       : str = ""
