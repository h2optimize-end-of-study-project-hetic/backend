from fastapi import FastAPI, Request, status
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware

from app.src.presentation.api.router import router
from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    contact={
        "name": settings.CONTACT_NAME,
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
    redoc_url=None
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


# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}

# @app.exception_handler(404)
# async def custom_404_handler():
#     return ({
#         "status_code":404,
#         "content":{"detail": "Route demandée non trouvée"}
#     })
