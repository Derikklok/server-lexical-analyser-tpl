# main.py
from fastapi import FastAPI
from app.api.endpoints import router  # Import the router

app = FastAPI()

# Include the router from the endpoints
app.include_router(router)