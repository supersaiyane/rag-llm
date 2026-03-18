def build_context(docs):

    context_parts = []

    for i, doc in enumerate(docs):

        text = doc.get("text", "")

        repo = doc.get("repo", "")
        path = doc.get("path", "")
        service = doc.get("service", "unknown")

        # build readable source
        source = path or service

        section = f"""
Document {i+1}
Source: {source}

{text}
"""

        context_parts.append(section)

    return "\n\n".join(context_parts)