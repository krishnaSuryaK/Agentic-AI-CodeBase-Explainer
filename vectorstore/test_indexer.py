from processing.chunker import chunk_code
from vectorstore.indexer import index_chunks


def main():

    code = """
def login(username, password):
    if username == "admin" and password == "1234":
        return "Login successful"

    return "Invalid credentials"


def logout(username):
    return f"{username} logged out"
"""

    # Step 1: Chunk the code
    chunks = chunk_code(
        content=code,
        file_path="auth.py",
        chunk_size=5
    )

    print(f"Created {len(chunks)} chunks.")

    # Step 2: Store chunks in Chroma
    index_chunks(chunks)


if __name__ == "__main__":
    main()