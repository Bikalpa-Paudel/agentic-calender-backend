from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .modules.users.user_router import router as UserRouter
app = FastAPI()
origins = [
        "http://localhost",
        "http://localhost:3000",
        "https://yourfrontend.com",
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # List of allowed origins
        allow_credentials=True,  # Allow cookies to be included in cross-origin requests
        allow_methods=["*"],  # List of allowed HTTP methods (e.g., ["GET", "POST"])
        allow_headers=["*"],  # List of allowed HTTP headers
    )

@app.get("/")
def root():
    return { "status": "up"}


app.include_router(UserRouter)
