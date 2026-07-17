import os
import sqlite3
import json
import copy
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "in0ri.db")

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.isoformat()}
        return super().default(obj)

def json_decoder(dct):
    if "__type__" in dct and dct["__type__"] == "datetime":
        return datetime.fromisoformat(dct["value"])
    return dct

class Database:
    def __init__(self, database_name):
        self.table_name = "collection_" + database_name
        # use check_same_thread=False for cross-thread access and timeout for concurrent writes
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("PRAGMA journal_mode=WAL;")
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, doc TEXT)")

    def _match(self, doc, query):
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True

    def insert_data(self, data):
        with self.conn:
            self.conn.execute(f"INSERT INTO {self.table_name} (doc) VALUES (?)", (json.dumps(data, cls=JSONEncoder),))
        return "inserted"

    def get_single_data(self, query):
        cursor = self.conn.execute(f"SELECT id, doc FROM {self.table_name}")
        for row in cursor:
            doc = json.loads(row["doc"], object_hook=json_decoder)
            if self._match(doc, query):
                return doc
        return None

    def get_multiple_data(self):
        cursor = self.conn.execute(f"SELECT doc FROM {self.table_name}")
        return [json.loads(row["doc"], object_hook=json_decoder) for row in cursor]

    def update_existing(self, unique, data_update):
        cursor = self.conn.execute(f"SELECT id, doc FROM {self.table_name}")
        for row in cursor:
            doc = json.loads(row["doc"], object_hook=json_decoder)
            if self._match(doc, unique):
                doc.update(data_update)
                with self.conn:
                    self.conn.execute(f"UPDATE {self.table_name} SET doc = ? WHERE id = ?", (json.dumps(doc, cls=JSONEncoder), row["id"]))
                return True
        return False

    def update_noexiting(self, unique, data_update):
        if not self.update_existing(unique, data_update):
            # Upsert
            new_doc = copy.deepcopy(unique)
            new_doc.update(data_update)
            self.insert_data(new_doc)
        return True

    def update_empty(self, unique, data_pull):
        # Empty array keys matching NoSQL $pull behavior for dict keys
        cursor = self.conn.execute(f"SELECT id, doc FROM {self.table_name}")
        for row in cursor:
            doc = json.loads(row["doc"], object_hook=json_decoder)
            if self._match(doc, unique):
                for k in data_pull.keys():
                    doc[k] = []
                with self.conn:
                    self.conn.execute(f"UPDATE {self.table_name} SET doc = ? WHERE id = ?", (json.dumps(doc, cls=JSONEncoder), row["id"]))
                return True
        return False

    def remove_data(self, query):
        cursor = self.conn.execute(f"SELECT id, doc FROM {self.table_name}")
        for row in cursor:
            doc = json.loads(row["doc"], object_hook=json_decoder)
            if self._match(doc, query):
                with self.conn:
                    self.conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (row["id"],))
                return True
        return False

