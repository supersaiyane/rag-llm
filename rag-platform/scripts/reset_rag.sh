#!/bin/bash

echo "======================================="
echo "RAG Platform Reset Script"
echo "======================================="

echo ""
echo "Starting core infrastructure..."

docker compose up -d postgres qdrant

sleep 3

echo ""
echo "Resetting Git ingestion registry..."

docker exec -i postgres psql -U raguser -d ragdb <<EOF
DO \$\$
BEGIN
   IF EXISTS (
      SELECT FROM information_schema.tables
      WHERE table_name = 'git_repositories'
   ) THEN
      DELETE FROM git_repositories;
   END IF;
END
\$\$;
EOF

echo "Git registry cleared."

echo ""
echo "Clearing Qdrant collection..."

curl -s -X DELETE http://localhost:6333/collections/engineering_knowledge > /dev/null

echo "Collection removed."

echo ""
echo "Recreating Qdrant collection..."

curl -s -X PUT http://localhost:6333/collections/engineering_knowledge \
-H "Content-Type: application/json" \
-d '{
  "vectors": {
    "size": 384,
    "distance": "Cosine"
  }
}' > /dev/null

echo "Collection created."

echo ""
echo "Starting remaining services..."

docker compose up -d ollama rag-api redis llm-gateway

sleep 5

echo ""
echo "Running ingestion..."

docker compose run --rm doc-ingestion

echo ""
echo "Checking vector count..."

VECTOR_COUNT=$(curl -s http://localhost:6333/collections/engineering_knowledge | jq '.result.points_count')

echo "Vectors indexed: $VECTOR_COUNT"

echo ""
echo "======================================="
echo "Reset completed successfully!"
echo "======================================="