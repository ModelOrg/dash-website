from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import nfl, r_integration

app = FastAPI(title="Sports Analytics API")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(nfl.router, prefix="/api/nfl", tags=["NFL"])
app.include_router(r_integration.router, prefix="/api/r", tags=["R Integration"])


@app.get("/")
def root():
    return {"message": "Sports Analytics API - See /docs for endpoints"}
