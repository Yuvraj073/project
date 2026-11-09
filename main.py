
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from database import check_database_connection

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


@app.get("/health/db")
def database_health_check():
    try:
        check_database_connection()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
    return {"status": "healthy", "database": "available"}
