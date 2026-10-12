"""
SIH PS 26239: Main FastAPI Application Entry Point
Mounts API routes, CORS middleware, and serves the UI frame
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.config import APP_NAME, VERSION, API_PREFIX
from app.api.routes import router

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Unified AI-Enabled Scholarship & Fellowship Management System for Ministry of Tribal Affairs (MoTA), Government of India"
)

# Enable CORS for cross-origin frontend support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(router, prefix=API_PREFIX, tags=["MoTA Scholarship APIs"])

# Static UI directory path
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_ui():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "app": APP_NAME,
        "version": VERSION,
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "version": VERSION}
