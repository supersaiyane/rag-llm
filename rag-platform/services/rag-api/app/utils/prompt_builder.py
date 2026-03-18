def build_prompt(question, docs):

    context = "\n".join([d["text"] for d in docs])

    prompt = f"""
    Use the following documentation to answer the question.

    Context:
    {context}

    Question:
    {question}
    """

    return prompt