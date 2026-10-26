from fastapi import FastAPI

app = FastAPI(
    title="SecureRAG",
    description="A secure document-grounded question-answering system",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SecureRAG",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }

