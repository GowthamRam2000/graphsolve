from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="GraphPuzzle API",
    description="Graph-Based Puzzle Solving Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "GraphPuzzle API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "GraphPuzzle API"}