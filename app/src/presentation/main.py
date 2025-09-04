import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.src.common.logging import setup_logging
from app.src.presentation.api.router import router
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    root_path=settings.API_PREFIX,
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
            "name": OpenApiTags.event,
            "description": "Les événements représentent des activités associées à une salle.",
        },
        {
            "name": OpenApiTags.event_room,
            "description": "Gestion entre les évènements et la salle",
        },
        {
            "name": OpenApiTags.map,
            "description": "Les maps correspondent aux images du plan d'un étage d'un bâtiment",
        },
        {
            "name": OpenApiTags.building,
            "description": "Gestion des bâtiments",
        },
        {
            "name": OpenApiTags.group,
            "description": "Gestion des groupes",
        },
        {
            "name": OpenApiTags.user_group,
            "description": "Gestion des groupes d'utilisateurs",
        },
    ],
    servers=settings.SERVERS
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
