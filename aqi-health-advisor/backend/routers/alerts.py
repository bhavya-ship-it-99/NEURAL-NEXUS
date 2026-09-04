from fastapi import APIRouter
import httpx
from ..database import get_connection
from ..config import WAQI_TOKEN
router=APIRouter()
@router.get('/')
async def alerts(lat:float,lon:float):
    async with httpx.AsyncClient(timeout=10) as c:
        a=await c.get(f'https://api.waqi.info/feed/geo:{lat};{lon}/',params={'token':WAQI_TOKEN}); w=await c.get('https://api.open-meteo.com/v1/forecast',params={'latitude':lat,'longitude':lon,'current':'temperature_2m,wind_speed_10m'})
    a.raise_for_status();w.raise_for_status(); ad=a.json(); wd=w.json().get('current',{});aqi=ad.get('data',{}).get('aqi') if ad.get('status')=='ok' else None;alerts=[]
    if aqi and aqi>150: alerts.append({'alert_type':'High AQI','message':f'AQI is {aqi}. Reduce outdoor exposure and consider protective measures.','severity':'high','timestamp':'Now'})
    elif aqi and aqi>100: alerts.append({'alert_type':'Elevated AQI','message':f'AQI is {aqi}. Sensitive people should reduce prolonged outdoor exertion.','severity':'medium','timestamp':'Now'})
    if wd.get('wind_speed_10m') and wd['wind_speed_10m']>35: alerts.append({'alert_type':'Strong wind','message':f'Wind is around {wd["wind_speed_10m"]} km/h. Take care with exposed outdoor activities.','severity':'medium','timestamp':'Now'})
    return {'alerts':alerts,'aqi':aqi,'temperature':wd.get('temperature_2m'),'wind_speed':wd.get('wind_speed_10m')}
