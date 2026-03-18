import httpx

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "phi3:mini"


async def rewrite_query(question: str):

    prompt = f"""
    Rewrite the user query to improve document retrieval.

    Rules:
    - Keep the same meaning.
    - Do NOT add new concepts.
    - Return ONLY the rewritten query.
    - Do NOT include explanations.

    User query:
    {question}

    Rewritten query:
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

        data = response.json()

        # Debug log
        print("Ollama rewrite response:", data)

        rewritten = data.get("response", "").strip()

        # remove accidental label text
        rewritten = rewritten.replace("Rewritten query:", "").strip()

        if not rewritten:
            rewritten = question
            
        # fallback if rewrite fails
        if not rewritten:
            return question

        # prevent overly aggressive rewriting
        if len(rewritten.split()) > 2 * len(question.split()):
            return question

        return rewritten

    except Exception as e:
        print("Rewrite error:", e)
        return question