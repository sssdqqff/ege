from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .routers import subject_router, topic_router, task_router, attempt_router, user_router

app = FastAPI(
    title="EGE API",
    debug=settings.debug_mode,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(subject_router)
app.include_router(topic_router)
app.include_router(task_router)
app.include_router(attempt_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the HELL"}
