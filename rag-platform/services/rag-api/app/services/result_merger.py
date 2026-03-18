def merge_results(vector_results, keyword_results):

    combined = {}

    for doc in vector_results:
        combined[doc["text"]] = doc

    for doc, score in keyword_results:
        if doc["text"] not in combined:
            combined[doc["text"]] = doc

    return list(combined.values())