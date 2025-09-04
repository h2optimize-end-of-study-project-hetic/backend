import logging
from typing import Annotated, Literal

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.src.presentation.core.config import settings
from app.src.presentation.core.open_api_tags import OpenApiTags


logger = logging.getLogger(__name__)

weather_router = APIRouter(prefix=f"/{OpenApiTags.weather.value}", tags=[OpenApiTags.weather])


Units = Literal["standard", "metric", "imperial"]


async def _call_openweather(path: str, params: dict) -> dict:
    if not settings.OPENWEATHER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENWEATHER_API_KEY manquant dans la configuration (.env)")

    url = f"{settings.OPENWEATHER_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    query = {"appid": settings.OPENWEATHER_API_KEY, **params}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=query)
    except httpx.RequestError as exc:
        logger.exception("Erreur de requête OpenWeather: %s", exc)
        raise HTTPException(status_code=502, detail="Impossible de contacter OpenWeather")

    if resp.status_code != 200:
        # Try to retrieve error message from OpenWeather
        try:
            payload = resp.json()
            message = payload.get("message") or payload
        except Exception:
            message = resp.text
        raise HTTPException(status_code=resp.status_code, detail=f"OpenWeather: {message}")

    return resp.json()


def _shape_current_weather(payload: dict) -> dict:
    return {
        "name": payload.get("name"),
        "coord": payload.get("coord"),
        "weather": payload.get("weather"),
        "main": payload.get("main"),  # temp, feels_like, pressure, humidity, etc.
        "wind": payload.get("wind"),
        "clouds": payload.get("clouds"),
        "dt": payload.get("dt"),
        "sys": payload.get("sys"),  # country, sunrise, sunset
    }


@weather_router.get(
    "/current",
    summary="Météo actuelle par ville",
    description="Récupère la météo actuelle depuis OpenWeather pour une ville donnée.",
)
async def get_current_by_city(
    city: str = Query(..., description="Nom de la ville, ex: Paris"),
    country: str | None = Query(None, description="Code pays ISO 3166, ex: FR"),
    units: Units = Query("metric", description="Unités: standard | metric | imperial"),
    lang: str = Query("fr", description="Langue des descriptions"),
):
    q = city if not country else f"{city},{country}"
    data = await _call_openweather(
        "/weather",
        params={"q": q, "units": units, "lang": lang},
    )
    return _shape_current_weather(data)


@weather_router.get(
    "/current/by-coords",
    summary="Météo actuelle par coordonnées",
    description="Récupère la météo actuelle depuis OpenWeather pour des coordonnées GPS.",
)
async def get_current_by_coords(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    units: Units = Query("metric", description="Unités: standard | metric | imperial"),
    lang: str = Query("fr", description="Langue des descriptions"),
):
    data = await _call_openweather(
        "/weather",
        params={"lat": lat, "lon": lon, "units": units, "lang": lang},
    )
    return _shape_current_weather(data)

