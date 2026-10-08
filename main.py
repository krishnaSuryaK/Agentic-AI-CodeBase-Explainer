from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.workflow import app as agent_app
from vectorstore.index_repository import index_repository

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AgenticAIPhenom",
    description="AI-powered GitHub repository analysis platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# Request models
# -----------------------------------------

class RepositoryRequest(BaseModel):

    owner: str
    repo: str


class QuestionRequest(BaseModel):

    question: str


# -----------------------------------------
# Health check
# -----------------------------------------

@app.get("/")
def root():

    return {
        "message": "AgenticAIPhenom API is running"
    }


# -----------------------------------------
# Index GitHub repository
# -----------------------------------------

@app.post("/repository/index")
async def index_repository_api(
    request: RepositoryRequest
):

    try:

        await index_repository(
            owner=request.owner,
            repo=request.repo
        )

        return {
            "status": "success",
            "message": (
                f"Repository "
                f"{request.owner}/{request.repo} "
                f"indexed successfully"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------------------
# Ask repository
# -----------------------------------------

@app.post("/ask")
def ask_repository(
    request: QuestionRequest
):

    try:

        result = agent_app.invoke(
            {
                "question": request.question,
                "category": "",
                "context": "",
                "answer": ""
            }
        )

        return {
            "question": request.question,
            "category": result["category"],
            "answer": result["answer"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        


# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain_ollama import ChatOllama
# from vectorstore.indexer import index_repository

# from github.loader import (
#     get_repository_contents,
#     get_file_content
# )

# from processing.chunker import chunk_code


# class RepositoryRequest(BaseModel):
#     github_url: str


# app = FastAPI(
#     title="Agentic AI Codebase Explainer",
#     description="AI-powered GitHub codebase analysis platform",
#     version="1.0.0"
# )


# llm = ChatOllama(
#     model="qwen2.5-coder:7b",
#     temperature=0
# )


# @app.get("/")
# def root():

#     return {
#         "message": "Agentic AI Codebase Explainer API is running!"
#     }


# @app.get("/health")
# def health_check():

#     return {
#         "status": "healthy"
#     }


# @app.get("/ask")
# def ask_ai(question: str):

#     response = llm.invoke(question)

#     return {
#         "question": question,
#         "answer": response.content
#     }


# def parse_github_url(github_url: str):

#     github_url = github_url.rstrip("/")

#     parts = github_url.split("/")

#     if len(parts) < 5:
#         raise ValueError(
#             "Invalid GitHub repository URL"
#         )

#     if parts[2] != "github.com":
#         raise ValueError(
#             "URL must be a GitHub URL"
#         )

#     owner = parts[3]
#     repo = parts[4]

#     return owner, repo


# @app.post("/repository/analyze")
# async def analyze_repository(
#     request: RepositoryRequest
# ):

#     owner, repo = parse_github_url(
#         request.github_url
#     )

#     files = await get_repository_contents(
#         owner,
#         repo
#     )

#     return {
#         "github_url": request.github_url,
#         "owner": owner,
#         "repository": repo,
#         "file_count": len(files),
#         "files": files
#     }


# @app.get("/repository/file")
# async def get_repository_file(
#     owner: str,
#     repo: str,
#     path: str
# ):

#     content = await get_file_content(
#         owner,
#         repo,
#         path
#     )

#     chunks = chunk_code(
#         content,
#         path
#     )

#     return {
#         "file": path,
#         "characters": len(content),
#         "chunks": chunks
#     }


# @app.post("/repository/index")
# async def index_github_repository(
#     request: RepositoryRequest
# ):

#     owner, repo = parse_github_url(
#         request.github_url
#     )

#     result = await index_repository(
#         owner,
#         repo
#     )

#     return {
#         "github_url": request.github_url,
#         "owner": owner,
#         "repository": repo,
#         "files_indexed": result["files"],
#         "chunks_indexed": result["chunks"]
#     }