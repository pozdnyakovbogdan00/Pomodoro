from handlers.ping import router as ping_router
from handlers.tasks import router as task_router
from handlers.users import router as user_router
from handlers.auth import router as auth_router

routes = [ping_router, task_router, user_router, auth_router]