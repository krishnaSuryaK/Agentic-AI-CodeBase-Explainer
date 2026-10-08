from .workflow import app


def main():

    question = (
        "What does the "
        "SpringCloudConfigServerApplication "
        "class do?"
    )

    result = app.invoke(
        {
            "question": question,
            "context": "",
            "answer": ""
        }
    )

    print("\nAI Answer")
    print("====================")

    print(result["answer"])


if __name__ == "__main__":
    main()