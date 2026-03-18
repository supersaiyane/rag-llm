import psycopg2
import hashlib
import os


class DocumentRegistry:

    def __init__(self):

        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )

        # ensure schema exists
        self.create_tables()

    def create_tables(self):

        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            source TEXT UNIQUE,
            service TEXT,
            doc_type TEXT,
            hash TEXT,
            indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # helpful index for faster lookups
        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_source
        ON documents(source);
        """)

        self.conn.commit()

    def compute_hash(self, text):
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def is_indexed(self, source, text):

        doc_hash = self.compute_hash(text)

        cur = self.conn.cursor()

        cur.execute(
            "SELECT hash FROM documents WHERE source=%s",
            (source,)
        )

        result = cur.fetchone()

        if not result:
            return False

        return result[0] == doc_hash

    def register(self, source, service, doc_type, text):

        doc_hash = self.compute_hash(text)

        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO documents
            (source, service, doc_type, hash)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (source)
            DO UPDATE SET hash=%s
            """,
            (source, service, doc_type, doc_hash, doc_hash)
        )

        self.conn.commit()