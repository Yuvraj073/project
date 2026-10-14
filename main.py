
from fastapi import FastAPI

app = FastAPI(
    title="JobTrack API",
    description="Track your job applications in one place.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to JobTrack!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
