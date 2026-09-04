from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.get("/")
async def get_forecast(lat: float, lon: float, days: int = 7):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,wind_speed_10m_max,relative_humidity_2m_max,weather_code",
        "forecast_days": days,
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, timeout=10)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Open-Meteo error: {e}")

    data = resp.json()
    daily = data.get("daily", {})

    dates = daily.get("time", [])
    result = []
    for i, date in enumerate(dates):
        result.append({
            "date": date,
            "temp_max": daily.get("temperature_2m_max", [None]*len(dates))[i],
            "temp_min": daily.get("temperature_2m_min", [None]*len(dates))[i],
            "wind_speed_max": daily.get("wind_speed_10m_max", [None]*len(dates))[i],
            "humidity_max": daily.get("relative_humidity_2m_max", [None]*len(dates))[i],
            "weather_code": daily.get("weather_code", [None]*len(dates))[i],
        })

    return {"forecast": result}