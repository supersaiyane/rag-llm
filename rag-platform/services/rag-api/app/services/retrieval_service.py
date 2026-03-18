import asyncio

from app.storage.vector_store import search_documents
from app.services.keyword_search import KeywordSearch
from app.services.reranker import Reranker
from app.services.service_detector import detect_service
from app.services.multi_query_generator import generate_query_variations

reranker = Reranker()


async def retrieve_docs(query):

    service = detect_service(query)

    queries = await generate_query_variations(query)

    async def vector_search():
        vector_docs = []

        for q in queries:
            results = search_documents(
                query=q,
                service=service
            )
            vector_docs.extend(results)

        if not vector_docs and service:
            vector_docs = search_documents(
                query=query,
                service=None
            )

        return vector_docs

    def keyword_search(vector_docs):
        engine = KeywordSearch(vector_docs)
        return engine.search(query)

    # run vector search first
    vector_docs = await vector_search()

    if not vector_docs:
        return []

    # run keyword search concurrently
    keyword_docs = await asyncio.to_thread(
        keyword_search,
        vector_docs
    )

    # merge results
    merged = {doc["text"]: doc for doc in vector_docs}

    for doc in keyword_docs:
        merged[doc["text"]] = doc

    merged_docs = list(merged.values())

    merged_docs = merged_docs[:40]

    final_docs = reranker.rerank(query, merged_docs)

    return final_docs[:6]