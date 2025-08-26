import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.src.common.logging import setup_logging
from app.src.presentation.api.router import router
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags
from app.src.presentation.core.open_api_events import OpenApiEvents
from app.src.presentation.core.open_api_maps import OpenApiMaps
from app.src.presentation.core.open_api_events import OpenApiEvents
from app.src.presentation.core.open_api_maps import OpenApiMaps

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    debug=settings.is_debug,
    redoc_url=None,
    openapi_url=settings.openapi_url,
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
            "name": OpenApiTags.tag,
            "description": "Les tags sont les capteurs matériels qui mesurent des valeurs dans le système.",
        },
        {
            "name": OpenApiTags.user,
            "description": "Gérer les utilisateurs (création, modification, suppression).",
        },
        {
            "name": OpenApiTags.tool,
            "description": "Données relatives au service",
        },
        {
            "name": OpenApiTags.auth,
            "description": "Authentification",
        },
        {
            "name": OpenApiTags.room,
            "description": "Gestion des salle au sein des organisations",
        },
        {
            "name": OpenApiMaps.map,
            "description": "Les maps correspondent aux images du plan d'un étage d'un bâtiment",
        },
        {
            "name": OpenApiEvents.event,
            "description": "Les événements représentent des activités associées à une salle.",
        },
        {
            "name": OpenApiMaps.map,
            "description": "Les maps correspondent aux images du plan d'un étage d'un bâtiment",
        },
        {
            "name": OpenApiEvents.event,
            "description": "Les événements représentent des activités associées à une salle.",
        },
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

