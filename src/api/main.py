"""
FastAPI backend for Fylum V2.0.0 GUI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.api.routes import config, operations, history, scheduler, notifications

app = FastAPI(
    title="Fylum API",
    description="REST API for Fylum file organizer",
    version="2.0.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(operations.router, prefix="/api/operations", tags=["operations"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(scheduler.router, prefix="/api/scheduler", tags=["scheduler"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "Fylum API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


def start_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the FastAPI server"""
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    start_server()
