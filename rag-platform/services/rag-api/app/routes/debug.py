from fastapi import APIRouter
from app.services.query_rewriter import rewrite_query
from app.storage.vector_store import search_documents
from app.services.keyword_search import KeywordSearch
from app.services.reranker import Reranker
from app.services.service_detector import detect_service

router = APIRouter()

reranker = Reranker()


@router.post("/debug/retrieval")
async def debug_retrieval(query: str):

    # Step 1: rewrite query
    rewritten = await rewrite_query(query)

    # Step 2: detect service
    service = detect_service(rewritten)

    # Step 3: vector search
    vector_docs = search_documents(
        query=rewritten,
        service=service
    )

    if not vector_docs and service:
        vector_docs = search_documents(query=rewritten, service=None)

    # Step 4: keyword search
    keyword_engine = KeywordSearch(vector_docs)
    keyword_docs = keyword_engine.search(rewritten)

    # Step 5: merge
    merged = {doc["text"]: doc for doc in vector_docs}

    for doc in keyword_docs:
        merged[doc["text"]] = doc

    merged_docs = list(merged.values())

    # Step 6: rerank
    reranked_docs = reranker.rerank(rewritten, merged_docs)

    # Step 7: final selection
    final_docs = reranked_docs[:6]

    return {
        "query": query,
        "rewritten_query": rewritten,
        "detected_service": service,
        "vector_results": vector_docs,
        "keyword_results": keyword_docs,
        "merged_results": merged_docs,
        "reranked_results": reranked_docs,
        "final_results": final_docs
    }