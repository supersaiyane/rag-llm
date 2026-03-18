from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.services.embedding_service import generate_embedding

client = QdrantClient(host="qdrant", port=6333)


COLLECTION = "engineering_knowledge"


def init_collection():

    collections = client.get_collections()

    names = [c.name for c in collections.collections]

    if COLLECTION not in names:

        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            ),
        )

        print(f"Created Qdrant collection: {COLLECTION}")
    else:
        print(f"Collection already exists: {COLLECTION}")


def index_document(doc_id, text, metadata):

    vector = generate_embedding(text)

    client.upsert(
        collection_name=COLLECTION,
        points=[
            {
                "id": doc_id,
                "vector": vector,
                "payload": {
                    "text": text,
                    **metadata
                }
            }
        ],
    )


def search_documents(query, service=None):

    vector = generate_embedding(query)

    search_filter = None

    if service:
        search_filter = {
            "must": [
                {
                    "key": "service",
                    "match": {
                        "value": service
                    }
                }
            ]
        }

    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=20,
        query_filter=search_filter
    )

    docs = []

    for point in results.points:

        payload = point.payload or {}

        docs.append({
            "text": payload.get("text"),
            "service": payload.get("service"),
            "type": payload.get("type"),
            "score": point.score
        })

    return docs