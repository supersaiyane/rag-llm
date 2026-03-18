import sys
sys.path.append("/app")

from app.storage.vector_store import init_collection, index_document


print("Initializing collection...")

init_collection()


print("Indexing test documents...")

index_document(
    1,
    "Redis failover procedure: promote replica node and restart master.",
    {
        "service": "redis",
        "type": "runbook"
    }
)

index_document(
    2,
    "Kafka restart procedure: restart broker and verify cluster health.",
    {
        "service": "kafka",
        "type": "runbook"
    }
)

index_document(
    3,
    "Postgres backup process: run pg_dump and upload to S3.",
    {
        "service": "postgres",
        "type": "runbook"
    }
)

print("Documents indexed successfully")