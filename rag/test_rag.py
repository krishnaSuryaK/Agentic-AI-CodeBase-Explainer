from rag.rag_service import ask_repository


def main():

    question = (
        "What does the "
        "SpringCloudConfigServerApplication class do?"
    )

    answer = ask_repository(question)

    print("\nAI Answer")
    print("====================")
    print(answer)


if __name__ == "__main__":
    main()