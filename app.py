import os
import streamlit as st
# import streamlit_ace as st_ace

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
        create_state(state, "acelang", "python")
        create_state(state, "acetheme", "tomorrow_night")
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
            create_state(state, "api_key", None)

        if is_api_key_valid(state.api_key, state) is not True:
            st.sidebar.text_input("Please enter OpenAI Key",key = 'api_key')
            st.stop()


StateInitializer(STATE)


class Handle:
    """Handle class for using tools """

    def __init__(self, name: str, content: str, template) :
        self.name       : str      = name
        self.menutitle  : str      = str.lower(name)
        self.description: str      = content
        self.template   : str      = template


# # generate 3 lists of strings, 3 strings long, 5,  and 10 long.. for testing... Unique...
# val1 = ["name" , "description", "template"]
# val2 = ["house", "chair", "tree", "car", "truck"]
# val3 = ["table", "dog", "cat", "bird", "chair", "tree", "car", "bee", "flower", "phone"]






# trig = STATE.get("trig", False)
# if not  trig:
#     STATE["t_1"] = "description"
#     STATE["t_2"] = "chair"
#     STATE["t_3"] = "dog"
#     STATE.trig = True

# st.radio('Select App', val3 , key="t_1")
# st.radio('Select App', val3 , key="t_2")
# st.radio('Select App', val3 , key="t_3")
