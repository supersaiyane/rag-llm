from app.services.retrieval_service import retrieve_docs
from app.services.query_rewriter import rewrite_query
from app.services.context_builder import build_context
from app.services.context_compressor import compress_context
import httpx


OLLAMA_URL = "http://ollama:11434/api/generate"


async def generate_answer(question, context):

    prompt = f"""
You are an internal engineering documentation assistant.

Use ONLY the provided documentation to answer.

Rules:
- Provide a clear explanation.
- Cite the exact source path from the context.
- Do NOT invent sources.
- If the answer is not in the context say:
  "No relevant documentation found."

Context:
{context}

Question:
{question}

Answer with sources:
"""

    payload = {
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120) as client:

        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

    result = response.json()

    print("LLM response:", result)

    answer = result.get("response")

    if not answer:
        return "No relevant documentation found."

    return answer.strip()


async def handle_query(question):

    # Step 1: rewrite the query
    rewritten = await rewrite_query(question)

    # Step 2: retrieve documents
    docs = await retrieve_docs(rewritten)

    docs = compress_context(rewritten, docs)
    
    # Step 3: build context
    compressed = compress_context(question, docs)

    context = "\n".join(compressed)
    # Step 4: generate answer
    answer = await generate_answer(question, context)

    return {
        "question": question,
        "rewritten_query": rewritten,
        "answer": answer,
        "documents": docs
    }