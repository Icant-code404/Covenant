from fastapi import FastAPI
from routers import upload, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Covenant Backend", version="1.0")

# Allow local React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Covenant API running!"}
