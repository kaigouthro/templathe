import os
import streamlit as st

from defaults import DefaultSettings
from constants import *
from utils import *
from state import PersistentState

from streamlit.runtime.state.session_state_proxy import SessionStateProxy
from langchain.llms import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain import hub

STATE  = PersistentState(SessionStateProxy, os.path.join(os.getcwd(),'session_state.pkl')).session_state_proxy()

llm = OpenAI(temperature=0)
from language_chain import llm, agent_executor, StateInitializer, Handle
from file_manager import read_file, write_file
from task_manager import execute_task, manage_tasks
from template_creator import create_prompt_template
from lemon_ai import integrate_with_lemon_ai
from openai_functions import use_openai_functions
    # Implement prompt template creation logic here
    pass

def integrate_with_lemon_ai():
    # Implement Lemon AI integration logic here
    pass

def use_openai_functions():
    # Implement OpenAI's function calling endpoints logic here
    pass

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