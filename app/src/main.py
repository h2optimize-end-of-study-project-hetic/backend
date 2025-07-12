import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

from app.src.common.logging import setup_logging
from app.src.presentation.api.router import router
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    debug=settings.is_debug,
    redoc_url=None,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    title=settings.PROJECT_NAME,
    swagger_favicon_url="/static/favicon.ico",
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    contact={
        "name": settings.CONTACT_NAME,
        "url": settings.CONTACT_URL,
        "email": settings.CONTACT_EMAIL,
    },
    license_info={
        "name": settings.LICENCE_NAME,
    },
    openapi_tags=[
        {
            "name": OpenApiTags.tags,
            "description": "Les tags sont les capteurs matériels qui mesurent des valeurs dans le système.",
        },
        {
            "name": OpenApiTags.users,
            "description": "Gérer les utilisateurs (création, modification, suppression).",
        }
    ],
    servers=settings.SERVERS,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)

app.mount("/static", StaticFiles(directory="app/src/presentation/static"), name="static")

@app.get("/")
async def root():
    return {
        "title":settings.PROJECT_NAME,
        "version":settings.VERSION,
        "env":settings.ENVIRONMENT,
        "log_level":settings.LOG_LEVEL,
        "debug": app.debug
    }
