class IngestionPipeline:

    def __init__(
        self,
        loader,
        chunker,
        embedder,
        vector_store,
        registry
    ):
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store
        self.registry = registry

    def run(self):

        documents = self.loader.load()

        for doc in documents:

            source = doc.metadata["source"]

            if self.registry.is_indexed(source, doc.text):
                print("Skipping:", source)
                continue

            # ------------------------------------------------
            # Extract metadata from filename
            # Example:
            # terraform__docs__planning-behaviors.md
            # ------------------------------------------------

            filename = source.split("/")[-1]

            parts = filename.split("__")

            repo = parts[0]

            file_path = "__".join(parts[1:]).replace(".md", "")
            file_path = file_path.replace("__", "/")

            service = repo

            # ------------------------------------------------
            # Chunk document
            # ------------------------------------------------

            chunks = self.chunker.chunk(doc.text)

            if not chunks:
                print(f"⚠️ No chunks generated, skipping: {source}")
                continue

            payloads = []
            texts = []

            for i, chunk in enumerate(chunks):

                payload = {
                    "repo": repo,
                    "service": service,
                    "file": file_path,
                    "source": source,
                    "source_system": doc.metadata.get("source_system", "filesystem"),
                    "type": doc.metadata.get("type", "documentation"),
                    "chunk_id": i,
                    "text": chunk
                }

                payloads.append(payload)
                texts.append(chunk)

            # ------------------------------------------------
            # Generate embeddings
            # ------------------------------------------------

            embeddings = self.embedder.embed(texts)

            # ------------------------------------------------
            # Store in vector DB
            # ------------------------------------------------

            self.vector_store.insert_batch(
                embeddings,
                payloads
            )

            # ------------------------------------------------
            # Register document in registry
            # ------------------------------------------------

            self.registry.register(
                source,
                service,
                payloads[0]["type"],
                doc.text
            )

            print(f"Indexed: {repo} -> {file_path}")