from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse

from api.routes.user import router as users_router
from api.routes.post import router as posts_router
from api.routes.attachment import router as attachments_router

app = FastAPI()
app.include_router(users_router, prefix="/users")
app.include_router(posts_router, prefix="/posts")
app.include_router(attachments_router, prefix="/attachments")


@app.get("/")
async def index():
    return RedirectResponse("/docs", status_code=status.HTTP_308_PERMANENT_REDIRECT)
