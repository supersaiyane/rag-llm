import httpx

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "phi3:mini"


def heuristic_queries(query: str):
    """
    Generate deterministic query variations.
    This ensures retrieval works even if LLM fails.
    """

    variations = []

    q = query.lower()

    variations.append(q)
    variations.append(f"{q} command")
    variations.append(f"{q} example")

    return variations


async def llm_queries(query: str):

    prompt = f"""
Generate 2 alternative search queries.

Rules:
- Preserve exact meaning
- Do not broaden the topic
- Do not introduce new concepts
- Only rephrase wording

Question:
{query}

Queries:
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

        data = response.json()

        text = data.get("response", "")

        queries = [
            q.strip()
            for q in text.split("\n")
            if q.strip()
        ]

        return queries[:2]

    except Exception as e:

        print("LLM query generation failed:", str(e))

        return []


async def generate_query_variations(query: str):

    queries = set()

    # heuristic queries
    queries.update(heuristic_queries(query))

    # LLM queries
    llm = await llm_queries(query)

    queries.update(llm)

    queries = list(queries)

    print("Hybrid queries:", queries)

    return queries