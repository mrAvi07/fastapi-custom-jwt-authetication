from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from apps.custom_auth.routers import router as auth_router
from apps.admin.routers import router as admin_router



app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


app.add_middleware(
	CORSMiddleware,
	allow_credentials=["*"],
	allow_headers=["*"],
	)


# routers path related to authentication
app.include_router(auth_router)
app.include_router(admin_router)