"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="To-Do App API",
    description="Backend API for the To-Do application",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Status response indicating the API is operational.
    """
    return {"status": "ok"}

