"""Database manager using aiosql for SQLite"""
import aiosql
import sqlite3
from pathlib import Path
from typing import Dict, List

class DatabaseManager:
    """Handles database operations with SQLite using raw SQL"""
    
    def __init__(self, db_url: str):
        self.db_path = db_url.split("///")[-1]
        self.queries = aiosql.from_path(
            Path(__file__).parent / "queries.sql",
            "sqlite3"
        )
        self._initialize_db()
        
    def _initialize_db(self):
        """Create tables if not exists"""
        with self._get_connection() as conn:
            self.queries.create_tables(conn)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Create new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def sync_user(self, user: Dict, roles: List[str]):
        """Synchronize user data with database"""
        with self._get_connection() as conn:
            # Update user details
            self.queries.upsert_user(conn, **user)
            # Update roles
            for role in roles:
                self.queries.set_roles(conn, user_id=user["id"], role=role)
    
    def get_user_roles(self, user_id: str) -> List[str]:
        """Retrieve user roles from database"""
        with self._get_connection() as conn:
            roles = self.queries.get_roles(conn, user_id=user_id)
            return [row["role"] for row in roles]