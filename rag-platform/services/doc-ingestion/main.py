import os
import sys
import shutil

from loaders.markdown_loader import MarkdownLoader
from chunker.semantic_chunker import SemanticChunker

from embeddings.embedding_service import EmbeddingService
from storage.qdrant_store import QdrantStore
from storage.postgres_registry import DocumentRegistry

from pipeline.ingestion_pipeline import IngestionPipeline

from config.settings import (
    ENABLE_FILESYSTEM,
    FILESYSTEM_DOC_PATH,
    ENABLE_GITHUB,
    GITHUB_REPOS
)

from connectors.github_connector import GithubConnector
from connectors.filesystem_connector import FilesystemConnector


def clean_docs_directory(docs_path):

    print("🧹 Cleaning docs directory")

    if not os.path.exists(docs_path):
        os.makedirs(docs_path)
        return

    for filename in os.listdir(docs_path):

        file_path = os.path.join(docs_path, filename)

        try:

            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:

            print(f"⚠️ Failed to delete {file_path}: {e}")


def main():

    print("🚀 Starting Document Ingestion Service")

    try:

        docs_path = os.getenv("DOCS_PATH", "/docs")
        print(f"📂 Using docs path: {docs_path}")

        # ------------------------------------------------
        # Step 0: Clean docs directory before ingestion
        # ------------------------------------------------

        clean_docs_directory(docs_path)

        # ------------------------------------------------
        # Step 1: Prepare documents from connectors
        # ------------------------------------------------

        print("🔌 Preparing ingestion sources...")

        # GitHub connector (runs first)
        if ENABLE_GITHUB:

            print("🐙 GitHub connector enabled")

            github_connector = GithubConnector(
                repos=GITHUB_REPOS,
                target_path=docs_path
            )

            github_connector.prepare()

        else:

            print("⏭ GitHub connector disabled")

        # Filesystem connector (runs second)
        if ENABLE_FILESYSTEM:

            print("📂 Filesystem connector enabled")

            fs_connector = FilesystemConnector(
                source_path=FILESYSTEM_DOC_PATH,
                target_path=docs_path
            )

            fs_connector.prepare()

        else:

            print("⏭ Filesystem connector disabled")

        print("✅ Source preparation complete")

        # ------------------------------------------------
        # Step 2: Initialize ingestion components
        # ------------------------------------------------

        print("⚙️ Initializing components...")

        loader = MarkdownLoader(docs_path)

        chunker = SemanticChunker(
            chunk_size=400,
            overlap=50
        )

        embedder = EmbeddingService()

        vector_store = QdrantStore()

        registry = DocumentRegistry()

        print("✅ Components initialized")

        # ------------------------------------------------
        # Step 3: Build ingestion pipeline
        # ------------------------------------------------

        pipeline = IngestionPipeline(
            loader,
            chunker,
            embedder,
            vector_store,
            registry
        )

        # ------------------------------------------------
        # Step 4: Run ingestion pipeline
        # ------------------------------------------------

        print("🚀 Running ingestion pipeline")

        pipeline.run()

        print("✅ Ingestion completed successfully")

    except Exception as e:

        print("❌ Ingestion service failed")
        print(str(e))

        import traceback
        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()