from fastapi import APIRouter, HTTPException
import httpx

from ..config import WAQI_TOKEN

router = APIRouter()

@router.get("/")
async def get_current_aqi(lat: float, lon: float):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": WAQI_TOKEN}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"WAQI error: {e}")

    data = resp.json()

    if data.get("status") != "ok":
        raise HTTPException(status_code=502, detail=f"WAQI returned: {data.get('data')}")

    d = data["data"]
    iaqi = d.get("iaqi", {})

    return {
        "aqi": d.get("aqi"),
        "station": d.get("city", {}).get("name"),
        "pm25": iaqi.get("pm25", {}).get("v"),
        "pm10": iaqi.get("pm10", {}).get("v"),
        "no2": iaqi.get("no2", {}).get("v"),
        "o3": iaqi.get("o3", {}).get("v"),
        "dominant_pollutant": d.get("dompol"),
    }
