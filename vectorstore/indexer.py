from langchain_core.documents import Document

from .chroma_store import get_vector_store


def index_chunks(chunks):

    vector_store = get_vector_store()

    documents = []
    ids = []

    for chunk in chunks:

        document = Document(
            page_content=chunk["content"],
            metadata={
                "file_path": chunk["file_path"],
                "language": chunk["language"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"]
            }
        )

        documents.append(document)

        chunk_id = (
            f'{chunk["file_path"]}:'
            f'{chunk["start_line"]}-'
            f'{chunk["end_line"]}'
        )

        ids.append(chunk_id)

    # Remove existing versions of these chunks
    vector_store.delete(ids=ids)

    # Add chunks to Chroma
    vector_store.add_documents(
        documents=documents,
        ids=ids
    )

    print(f"Indexed {len(documents)} chunks.")

    return vector_store