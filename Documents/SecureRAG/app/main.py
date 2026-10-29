
from fastapi import FastAPI

from SecureRAG.api.documents import router as documents_router

app = FastAPI(
    title="SecureRAG",
    description="Secure enterprise knowledge retrieval system",
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
