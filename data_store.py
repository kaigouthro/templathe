import sqlite3


class ItemsDatabase:

    def __init__(self, filepath):
        # Create a connection to the database
        self.conn = sqlite3.connect(filepath)
        # Create a cursor
        self.c = self.conn.cursor()
        # Create a table to store the items
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT,
            data_type TEXT,
            data_value TEXT
        )"""
        )

    def set(self, tool_name, data_type, data_value):
        # Check if the item already exists for the specified tool
        self.c.execute("SELECT tool_name FROM items WHERE tool_name = ?", (tool_name,))
        existing_item = self.c.fetchone()

        if existing_item:
            # Update the existing item
            self.c.execute(
                "UPDATE items SET data_type = ?, data_value = ? WHERE tool_name = ?",
                (data_type, data_value, tool_name),
            )
        else:
            # Insert a new item into the database
            self.c.execute(
                "INSERT INTO items (tool_name, data_type, data_value) VALUES (?, ?, ?)",
                (tool_name, data_type, data_value),
            )

        # Commit the changes to the database
        self.conn.commit()

    def get(self, tool_name):
        # Get all the items for the specified tool
        self.c.execute("SELECT data_type, data_value FROM items WHERE tool_name = ?", (tool_name,))
        return self.c.fetchall()

    def remove(self, tool_name):
        # Remove the specified item from the database
        self.c.execute("DELETE FROM items WHERE tool_name = ?", (tool_name,))

        # Commit the changes to the database
        self.conn.commit()

    def close(self):
        # Close the connection to the database
        self.conn.close()



import json
import os
import streamlit as st


class DataStorage:
    def __init__(self, root_folder):
        self.root = root_folder
        os.makedirs(self.root, exist_ok=True)
        st.session_state["root_folder"] = self.root

    def save_setting(self, setting: str):
        filename = os.path.join(self.root, f"{setting}.json")
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(st.session_state[f"{setting}"], json_file)

    def load_setting(self, setting: str):
        filename = os.path.join(self.root, f"{setting}.json")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as json_file:
                content = json.load(json_file)
                st.session_state[f"{setting}"] = content
                return content
        else:
            with open(filename, "w", encoding="utf-8") as json_file:
                new_setting = (
                    {}
                    if setting not in st.session_state
                    else st.session_state[f"{setting}"]
                )
                json.dump(new_setting, json_file)

    def access_setting(self, setting, do_save: bool = True):
        if do_save:
            self.save_setting(setting)
        else:
            self.load_setting(setting)

    def load_list(self, settings: list):
        if settings is None:
            settings = []
        prog = st.progress(len(settings), "Loading Settings")
        with prog:
            for set in settings:
                try:
                    self.load_setting(set)
                except Exception:
                    pass
                prog.progress(settings.index(set) / len(settings))
