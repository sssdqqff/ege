from .subject import router as subject_router
from .topic import router as topic_router
from .task import router as task_router
from .attempt import router as attempt_router
from .user import router as user_router

__all__ = [
    "subject_router",
    "topic_router",
    "task_router",
    "attempt_router",
    "user_router"
]