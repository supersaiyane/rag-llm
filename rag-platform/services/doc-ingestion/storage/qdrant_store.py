import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantStore:

    def __init__(self):

        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))

        self.client = QdrantClient(host=host, port=port)

        self.collection = "engineering_knowledge"

        # Ensure collection exists
        self.create_collection()

    def create_collection(self):

        collections = self.client.get_collections().collections
        names = [c.name for c in collections]

        if self.collection not in names:

            print(f"Creating Qdrant collection: {self.collection}")

            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=384,   # embedding size for all-MiniLM-L6-v2
                    distance=Distance.COSINE
                )
            )

    def insert_batch(self, embeddings, payloads):

        points = []

        for vector, payload in zip(embeddings, payloads):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection,
            points=points
        )