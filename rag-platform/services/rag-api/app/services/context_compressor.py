import re

def compress_context(query, docs):

    keywords = set(query.lower().split())

    filtered_docs = []

    for doc in docs:

        text = doc.get("text", "")

        sentences = re.split(r'(?<=[.!?]) +', text)

        selected = []

        for s in sentences:

            words = set(s.lower().split())

            if keywords & words:
                selected.append(s)

        if selected:
            doc_copy = doc.copy()
            doc_copy["text"] = " ".join(selected)
            filtered_docs.append(doc_copy)

    return filtered_docs