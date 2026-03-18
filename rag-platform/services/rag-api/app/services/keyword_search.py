from rank_bm25 import BM25Okapi


class KeywordSearch:

    def __init__(self, documents):

        self.documents = documents
        self.corpus = [doc["text"].split() for doc in documents]
        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query, top_k=20):

        tokens = query.split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked[:top_k]]