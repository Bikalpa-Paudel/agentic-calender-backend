from fastapi import FastAPI
from .modules.users.user_router import router as UserRouter

app = FastAPI()

@app.get("/")
def root():
    return { "status": "up"}

app.include_router(UserRouter)
