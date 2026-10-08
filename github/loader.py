import httpx
import base64
import os
from dotenv import load_dotenv


GITHUB_API = "https://api.github.com"

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
}


ALLOWED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".sql",
    ".json",
    ".xml",
    ".yml",
    ".yaml",
    ".md",
}


# ---------------------------------------------------------
# METHOD 1
# Get all useful files from a GitHub repository
# ---------------------------------------------------------

async def get_repository_contents(owner: str, repo: str):

    headers = get_github_headers()

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=60.0
    ) as client:

        # Get repository information
        repo_url = f"{GITHUB_API}/repos/{owner}/{repo}"

        repo_response = await client.get(
            repo_url,
            headers=headers
        )

        if repo_response.status_code != 200:
            raise Exception(
                f"GitHub repository API error: "
                f"{repo_response.status_code}: "
                f"{repo_response.text}"
            )

        repo_data = repo_response.json()

        # Get canonical repository information
        canonical_owner = repo_data["owner"]["login"]
        canonical_repo = repo_data["name"]

        # Get default branch
        default_branch = repo_data["default_branch"]

        print("Canonical owner:", canonical_owner)
        print("Canonical repository:", canonical_repo)
        print("Default branch:", default_branch)

        # Get repository tree
        tree_url = (
            f"{GITHUB_API}/repos/"
            f"{canonical_owner}/{canonical_repo}"
            f"/git/trees/{default_branch}?recursive=1"
        )

        tree_response = await client.get(
            tree_url,
            headers=headers
        )

        if tree_response.status_code != 200:
            raise Exception(
                f"GitHub tree API error: "
                f"{tree_response.status_code}: "
                f"{tree_response.text}"
            )

        data = tree_response.json()

    files = []

    for item in data.get("tree", []):

        # We only want files, not folders
        if item["type"] != "blob":
            continue

        path = item["path"]

        # Ignore unnecessary directories
        if any(
            directory in path.split("/")
            for directory in IGNORED_DIRECTORIES
        ):
            continue

        # Keep only useful file types
        if not any(
            path.endswith(extension)
            for extension in ALLOWED_EXTENSIONS
        ):
            continue

        files.append({
            "path": path,
            "url": (
                f"https://github.com/"
                f"{canonical_owner}/"
                f"{canonical_repo}/blob/"
                f"{default_branch}/"
                f"{path}"
            )
        })

    return files


# ---------------------------------------------------------
# METHOD 2
# Get the actual content of one file
# ---------------------------------------------------------

async def get_file_content(
    owner: str,
    repo: str,
    path: str
):

    headers = get_github_headers()

    url = (
        f"{GITHUB_API}/repos/"
        f"{owner}/{repo}/contents/"
        f"{path}"
    )

    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=60.0
    ) as client:

        response = await client.get(
            url,
            headers=headers
        )

    if response.status_code != 200:
        raise Exception(
            f"GitHub file API error: "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    # GitHub normally returns file content as Base64
    if data.get("encoding") != "base64":
        raise Exception(
            "Unexpected GitHub file encoding"
        )

    # Decode Base64 → actual source code
    content = base64.b64decode(
        data["content"]
    ).decode(
        "utf-8",
        errors="ignore"
    )

    return content

def get_github_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers