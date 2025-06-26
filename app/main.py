from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import casting
from app.db.database import engine
from app.models import casting as casting_models

# Create database tables
casting_models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Casting Number Lookup API",
    description="API for looking up casting numbers and their associated data",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(
    casting.router,
    prefix="/api/castings",
    tags=["castings"],
)


@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to the Casting Number Lookup API",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
