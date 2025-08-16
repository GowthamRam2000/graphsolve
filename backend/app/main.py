from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="GraphPuzzle API",
    description="Graph-Based Puzzle-Solving Platform",
    version="1.0.0",
)

# register all API routes first
app.include_router(router, prefix="/api")

# add CORS middleware so it wraps every route, including OPTIONS pre-flights
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://graphsolvefrontend.onrender.com"],  # restrict to your frontend URL for production security
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# basic health checks
@app.get("/")
async def root():
    return {"message": "GraphPuzzle API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "GraphPuzzle API"}
