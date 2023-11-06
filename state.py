import streamlit as st
import pickle

class PersistentState:
    def __init__(self, session_state_proxy, filename):
        self.session_state_proxy = session_state_proxy
        self.filename = filename
        self.load_state()

    def load_state(self):
        try:
            with open(self.filename, 'rb') as file:
                state = pickle.load(file)
        except FileNotFoundError:
            state = {}
        self.session_state_proxy.update(state)

    def persist_state(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.session_state_proxy.to_dict(), file)

    def __dict__(self):
        self.session_state_proxy.__dict__()
