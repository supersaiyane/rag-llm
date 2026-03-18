#!/bin/bash

echo "====================================="
echo "RAG Platform Demo Startup"
echo "====================================="

echo ""
echo "Starting infrastructure..."

docker compose up -d postgres qdrant ollama rag-api

echo ""
echo "Waiting for services..."

sleep 5

echo ""
echo "Running ingestion..."

docker compose run --rm doc-ingestion

echo ""
echo "Checking vector count..."

VECTOR_COUNT=$(curl -s http://localhost:6333/collections/engineering_knowledge | jq '.result.points_count')

echo "Vectors indexed: $VECTOR_COUNT"

if [ "$VECTOR_COUNT" -le 0 ]; then
  echo "❌ Ingestion failed"
  exit 1
fi

echo ""
echo "Running demo queries..."

echo ""
echo "Query 1: Redis recovery"

curl -s -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
"user_id":"demo",
"question":"How do we recover Redis?"
}' | jq

echo ""
echo "-------------------------------------"

echo ""
echo "Query 2: Terraform plan"

curl -s -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
"user_id":"demo",
"question":"What does terraform plan do?"
}' | jq

echo ""
echo "-------------------------------------"

echo ""
echo "Query 3: Kafka restart"

curl -s -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
"user_id":"demo",
"question":"How do we restart Kafka?"
}' | jq

echo ""
echo "====================================="
echo "Demo Completed"
echo "====================================="