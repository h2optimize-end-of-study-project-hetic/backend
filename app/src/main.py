from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.src.presentation.api.router import router
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags

app = FastAPI(
    debug=settings.is_debug,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
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
    redoc_url=None,
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


@app.get("/")
async def root():
    return {
        "title":settings.PROJECT_NAME,
        "version":settings.VERSION,
        "env":settings.ENVIRONMENT,
        "log_level":settings.LOG_LEVEL,
        "debug": app.debug
    }
