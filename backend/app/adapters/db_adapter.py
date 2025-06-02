import sqlite3
from typing import Any, List, Tuple, Optional

class SQLiteDBAdapter:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def execute(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> None:
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            
    def create_table(self, table_name: str, columns: str) -> None:
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute(query)

    def fetch_one(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple[Any, ...]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple[Any, ...]]:
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        
    def add_question(self, section: str, question_type: str, difficulty: int, description: str, count: int) -> None:
        query = """
        INSERT INTO questions (section, questionType, difficulty, description)
        VALUES (?, ?, ?, ?)
        """
        self.execute(query, (section, question_type, difficulty, description))