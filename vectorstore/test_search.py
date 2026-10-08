from vectorstore.chroma_store import get_vector_store


def main():

    vector_store = get_vector_store()

    question = "How does the login function authenticate the user?"

    results = vector_store.similarity_search(
        question,
        k=2
    )

    print("\nSearch results:")
    print("================")

    for result in results:
        print("File:", result.metadata["file_path"])
        print(
            "Lines:",
            result.metadata["start_line"],
            "-",
            result.metadata["end_line"]
        )
        print("Language:", result.metadata["language"])
        print("Code:")
        print(result.page_content)
        print("----------------")


if __name__ == "__main__":
    main()