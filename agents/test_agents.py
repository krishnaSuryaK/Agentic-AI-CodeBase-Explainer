from .workflow import app


def ask(question):

    result = app.invoke(
        {
            "question": question,
            "category": "",
            "context": "",
            "answer": ""
        }
    )

    print("\n==============================")
    print("QUESTION")
    print("==============================")
    print(question)

    print("\nANSWER")
    print("==============================")
    print(result["answer"])


def main():

    # Test 1
    ask(
        "What does the SpringCloudConfigServerApplication class do?"
    )

    # Test 2
    ask(
        "Are there any potential bugs or problems in the code?"
    )

    # Test 3
    ask(
        "Explain how the Netflix Zuul API gateway works."
    )


if __name__ == "__main__":
    main()