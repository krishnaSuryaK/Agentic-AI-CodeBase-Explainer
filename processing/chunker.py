def get_language(file_path: str):

    extension = file_path.split(".")[-1].lower()

    language_map = {
        "py": "python",
        "java": "java",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "html": "html",
        "css": "css",
        "scss": "scss",
        "sql": "sql",
        "json": "json",
        "xml": "xml",
        "yml": "yaml",
        "yaml": "yaml",
        "md": "markdown"
    }

    return language_map.get(
        extension,
        "unknown"
    )


def chunk_code(
    content: str,
    file_path: str,
    chunk_size: int = 100
):

    lines = content.splitlines()

    language = get_language(file_path)

    chunks = []

    for start in range(
        0,
        len(lines),
        chunk_size
    ):

        end = min(
            start + chunk_size,
            len(lines)
        )

        chunk = "\n".join(
            lines[start:end]
        )

        chunks.append({
            "content": chunk,
            "file_path": file_path,
            "language": language,
            "start_line": start + 1,
            "end_line": end
        })

    return chunks