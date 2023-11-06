import tiktoken
import openai
import os
from  streamlit.runtime.state.session_state_proxy import SessionStateProxy
import streamlit as st


def is_api_key_valid(key, state : SessionStateProxy):
    try:
        if response := openai.ChatCompletion.create(
            engine="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "This is a test."}],
            max_tokens=10,
            api_key=key,
        ):
            return True
    except Exception:
        st.error('Invvalid key')
        return False



def tikinstaller(state: SessionStateProxy):
    state.encodings = tiktoken.list_encoding_names()
    state.encodings.reverse()


def set_to_state(state: SessionStateProxy, name, default=None):
    if name not in state:
        state[name] = default
        return


def get_api_key(state : SessionStateProxy):
    api_key = None if "api_key" not in state else state["api_key"]
    if api_key is not None:
        return api_key
    else:
        api_key = os.environ["OPENAI_API_KEY"] or None

    if api_key:
        state["api_key"] = api_key
        return api_key


def get_models(state : SessionStateProxy):
    """get modelsavailable from openai"""
    resp = openai.Model.list()
    m = [m["id"] for m in resp.data]  # type: ignore
    model_ids = [model for model in m if "gpt" in model]
    model_ids.sort()
    set_to_state(state, "models", model_ids)
    return


def tokencount(string):
    """Returns the number of tokens in a text string."""
    tokens = tiktoken.get_encoding("cl100k_base").encode(string or "buffer")
    return len(tokens)
