from data_store import ItemsDatabase
from constants import *

class DefaultSettings:
    def __init__(self, state):
        self.set_defaults(state)

    def set_defaults(self, state):
        """ needs default settings in here"""
        state[SETTINGS] = {

        }
