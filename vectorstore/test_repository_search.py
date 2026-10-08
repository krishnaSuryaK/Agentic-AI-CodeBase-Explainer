from vectorstore.chroma_store import get_vector_store


def main():

    vector_store = get_vector_store()

    question = "What does the SpringCloudConfigServerApplication class do?"

    results = vector_store.similarity_search(
        question,
        k=3
    )

    print("\nSearch Results")
    print("====================")

    for result in results:

        print("\nFile:", result.metadata["file_path"])

        print(
            "Lines:",
            result.metadata["start_line"],
            "-",
            result.metadata["end_line"]
        )

        print("Language:", result.metadata["language"])

        print("\nCode:")
        print(result.page_content)

        print("\n--------------------")


if __name__ == "__main__":
    main()