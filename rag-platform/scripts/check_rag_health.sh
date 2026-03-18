#!/bin/bash

echo "====================================="
echo "RAG Platform Health Check"
echo "====================================="

echo ""
echo "Checking Docker containers..."

docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "rag-api|qdrant|postgres|ollama"

echo ""
echo "Checking RAG API..."

API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$API_STATUS" = "200" ]; then
  echo "✅ RAG API is healthy"
else
  echo "❌ RAG API is NOT responding"
fi

echo ""
echo "Checking Qdrant..."

QDRANT_STATUS=$(curl -s http://localhost:6333/collections | jq '.result.collections | length')

if [ "$QDRANT_STATUS" -ge 1 ]; then
  echo "✅ Qdrant reachable"
else
  echo "❌ Qdrant problem"
fi

echo ""
echo "Checking vector count..."

VECTOR_COUNT=$(curl -s http://localhost:6333/collections/engineering_knowledge | jq '.result.points_count')

echo "Vectors indexed: $VECTOR_COUNT"

if [ "$VECTOR_COUNT" -gt 0 ]; then
  echo "✅ Vector DB populated"
else
  echo "⚠️ Vector DB empty"
fi

echo ""
echo "Checking Ollama model..."

OLLAMA_STATUS=$(curl -s http://localhost:11434/api/tags | jq '.models[].name' | grep phi3)

if [ -n "$OLLAMA_STATUS" ]; then
  echo "✅ Ollama model available"
else
  echo "❌ Ollama model missing"
fi

echo ""
echo "====================================="
echo "Health Check Complete"
echo "====================================="