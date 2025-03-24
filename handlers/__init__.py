from handlers.ping import router as ping_router
from handlers.tasks import router as task_router

routes = [ping_router, task_router]