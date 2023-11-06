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

