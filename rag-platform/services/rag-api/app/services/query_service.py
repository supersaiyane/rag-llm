from app.services.retrieval_service import retrieve_docs
from app.services.llm_client import generate_answer
from app.utils.prompt_builder import build_prompt

async def handle_query(question):

    docs = await retrieve_docs(question)

    prompt = build_prompt(question, docs)

    answer = await generate_answer(prompt)

    return {
        "answer": answer,
        "sources": docs
    }