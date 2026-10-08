import asyncio

from github.loader import (
    get_repository_contents,
    get_file_content
)

from processing.chunker import chunk_code

from .indexer import index_chunks


async def index_repository(
    owner: str,
    repo: str
):

    print(f"Indexing repository: {owner}/{repo}")

    # -----------------------------------------
    # 1. Get useful files from GitHub
    # -----------------------------------------

    files = await get_repository_contents(
        owner,
        repo
    )

    print(f"Found {len(files)} useful files.")

    all_chunks = []

    # -----------------------------------------
    # 2. Download and chunk every file
    # -----------------------------------------

    for index, file in enumerate(files, start=1):

        path = file["path"]

        print(
            f"[{index}/{len(files)}] "
            f"Processing: {path}"
        )

        try:

            content = await get_file_content(
                owner,
                repo,
                path
            )

            chunks = chunk_code(
                content=content,
                file_path=path
            )

            all_chunks.extend(chunks)

        except Exception as e:

            print(
                f"Failed to process {path}: {e}"
            )

    # -----------------------------------------
    # 3. Store all chunks in Chroma
    # -----------------------------------------

    print(
        f"\nTotal chunks created: "
        f"{len(all_chunks)}"
    )

    if not all_chunks:
        print("No chunks to index.")
        return

    index_chunks(all_chunks)

    print("\nRepository indexing complete!")


if __name__ == "__main__":

    asyncio.run(
        index_repository(
            owner="krishnaSuryaK",
            repo="MicroServices-with-springBoot-and-SpringCloud"
        )
    )   