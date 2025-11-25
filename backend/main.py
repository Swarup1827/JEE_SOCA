from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes
import uvicorn

app = FastAPI(title="JEE SOCA Analysis API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Backend is running! If you see this, the Frontend is not being served correctly."}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
