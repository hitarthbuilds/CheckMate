from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze

app = FastAPI(
    title="Fake News Detection (Multilingual, Real-time)",
    description="Zero-shot multilingual fake-news detection with credibility scoring",
    version="1.0"
)

# Allow local browsers / frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "Fake News Detection API (multilingual) is running"}
