from langchain_core.documents import Document

from .chroma_store import get_vector_store


def main():

    # Get Chroma
    vector_store = get_vector_store()

    # Clear old test data
    vector_store.delete_collection()

    # Create a fresh collection
    vector_store = get_vector_store()

    # Sample documents
    documents = [
        Document(
            page_content="The login function validates the user's email and password.",
            metadata={
                "file": "auth.py",
                "language": "python"
            }
        ),
        Document(
            page_content="The database connection uses PostgreSQL to store user information.",
            metadata={
                "file": "database.py",
                "language": "python"
            }
        ),
        Document(
            page_content="The payment function processes credit card transactions.",
            metadata={
                "file": "payment.py",
                "language": "python"
            }
        )
    ]

    # Add documents
    vector_store.add_documents(documents)

    print("Documents added to Chroma successfully!")

    # Search
    question = "How does the application authenticate users?"

    results = vector_store.similarity_search(
        question,
        k=2
    )

    print("\nSearch results:")
    print("----------------")

    for result in results:
        print("File:", result.metadata["file"])
        print("Language:", result.metadata["language"])
        print("Content:", result.page_content)
        print("----------------")


if __name__ == "__main__":
    main()