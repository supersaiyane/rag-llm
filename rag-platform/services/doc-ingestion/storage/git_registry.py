import sqlite3
import os
from datetime import datetime


DB_PATH = os.getenv("GIT_REGISTRY_DB", "/data/git_registry.db")


class GitRegistry:

    def __init__(self):

        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        self.conn = sqlite3.connect(DB_PATH)

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS git_repos (
                repo TEXT PRIMARY KEY,
                commit_sha TEXT,
                updated_at TEXT
            )
            """
        )

    def get_commit(self, repo):

        cursor = self.conn.execute(
            "SELECT commit_sha FROM git_repos WHERE repo = ?",
            (repo,)
        )

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    def update_commit(self, repo, sha):

        self.conn.execute(
            """
            INSERT OR REPLACE INTO git_repos(repo, commit_sha, updated_at)
            VALUES (?, ?, ?)
            """,
            (repo, sha, datetime.utcnow().isoformat())
        )

        self.conn.commit()