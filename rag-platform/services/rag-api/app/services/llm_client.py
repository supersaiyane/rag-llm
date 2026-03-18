import httpx
import asyncio
import time
import uuid

MODEL = "phi3:mini"

OLLAMA_SERVERS = [
    "http://ollama:11434",
    "http://ollama2:11434",
    "http://ollama3:11434"
]

TIMEOUT = 120

# round-robin counter
server_index = 0

# lock for concurrency safety
lock = asyncio.Lock()


async def get_next_server():
    global server_index

    async with lock:
        server = OLLAMA_SERVERS[server_index % len(OLLAMA_SERVERS)]
        server_index += 1
        return server


async def generate_answer(prompt: str):

    request_id = str(uuid.uuid4())[:8]

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.1
        }
    }

    server = await get_next_server()

    url = f"{server}/api/generate"

    print(f"[{request_id}] 🚀 Selected LLM server: {server}")

    start = time.time()

    try:

        async with httpx.AsyncClient(timeout=TIMEOUT) as client:

            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

        latency = round(time.time() - start, 2)

        print(f"[{request_id}] ⏱ LLM latency: {latency}s")

        if response.status_code != 200:
            print(f"[{request_id}] ❌ OLLAMA ERROR: {response.text}")
            return ""

        data = response.json()

        print(f"[{request_id}] ✅ Response received from {server}")

        return data.get("response", "").strip()

    except Exception as e:

        print(f"[{request_id}] ❌ Request failed for {server}: {e}")

        return ""