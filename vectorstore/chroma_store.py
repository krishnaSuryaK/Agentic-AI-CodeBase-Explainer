from pathlib import Path

from langchain_chroma import Chroma

from .embeddings import get_embedding_model


CHROMA_DIR = Path(__file__).resolve().parent.parent / "chroma_db"


def get_vector_store():
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name="code_chunks",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_DIR)
    )

    return vector_store