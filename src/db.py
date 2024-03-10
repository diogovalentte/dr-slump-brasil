import sqlite3


class DB:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS downloaded (name TEXT)")
        conn.commit()
        conn.close()

    def insert(self, name: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO downloaded VALUES (?)", (name,))
        conn.commit()
        conn.close()

    def select(self, name: str):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM downloaded WHERE name=?", (name,))
        row = cur.fetchone()
        conn.close()

        return row
