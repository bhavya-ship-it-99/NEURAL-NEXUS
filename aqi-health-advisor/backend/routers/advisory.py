from fastapi import APIRouter, HTTPException
import httpx, json
from ..models import AdvisoryRequest
from ..database import get_connection
from ..config import GROQ_API_KEY
router=APIRouter()

def fallback(aqi,temp,profile):
    hist=(profile.medical_history if profile else [])
    risk='Low'
    if aqi is not None and aqi>150:risk='High'
    elif aqi is not None and aqi>100:risk='Elevated'
    elif aqi is not None and aqi>50:risk='Moderate'
    precautions=[]
    if aqi and aqi>50:precautions.append('Reduce prolonged outdoor exertion while air quality is elevated.')
    if aqi and aqi>100:precautions.append('Consider a well-fitted mask for longer outdoor exposure.')
    if any(h in hist for h in ['Asthma','COPD','Allergies','Heart condition']):precautions.append('Because of your profile, keep your reliever/usual care plan available and watch for symptoms.')
    if temp is not None and temp>=35:precautions.append('Hydrate regularly and avoid strenuous activity during peak heat.')
    if not precautions:precautions=['Outdoor activity is reasonable based on the current snapshot; keep normal hydration and awareness.']
    return risk,'Current conditions look '+('challenging.' if risk in ['High','Elevated'] else 'manageable.'),precautions
@router.post('/')
async def advisory(req:AdvisoryRequest):
    async with httpx.AsyncClient(timeout=10) as client:
        w=await client.get('https://api.open-meteo.com/v1/forecast',params={'latitude':req.lat,'longitude':req.lon,'current':'temperature_2m,relative_humidity_2m,wind_speed_10m'})
        a=await client.get(f'https://api.waqi.info/feed/geo:{req.lat};{req.lon}/',params={'token':WAQI_TOKEN})
    w.raise_for_status(); a.raise_for_status(); wd=w.json().get('current',{}); ad=a.json()
    if ad.get('status')!='ok': raise HTTPException(502,f"WAQI returned: {ad.get('data')}")
    aqi=ad['data'].get('aqi'); temp=wd.get('temperature_2m'); hum=wd.get('relative_humidity_2m'); wind=wd.get('wind_speed_10m'); profile=req.profile
    risk,text,precautions=fallback(aqi,temp,profile)
    if GROQ_API_KEY:
        try:
            from groq import Groq
            client=Groq(api_key=GROQ_API_KEY)
            prompt=f"Give concise environmental health guidance. AQI={aqi}, temp={temp}C, humidity={hum}%, wind={wind}km/h. Age group={profile.age_group if profile else '18-39'}, medical history={profile.medical_history if profile else []}, occupation={profile.occupation if profile else ''}. Return JSON with keys risk_level, advisory_text, precautions (array). No diagnosis."
            r=client.chat.completions.create(model=GROQ_MODEL,messages=[{'role':'system','content':'You are a careful environmental health information assistant.'},{'role':'user','content':prompt}],temperature=.2,response_format={'type':'json_object'})
            out=json.loads(r.choices[0].message.content); risk=out.get('risk_level',risk); text=out.get('advisory_text',text); precautions=out.get('precautions',precautions)
        except Exception: pass
    conn=get_connection(); conn.execute('INSERT INTO advisory_history(timestamp,lat,lon,aqi,temp,humidity,wind_speed,advisory_text,precautions) VALUES(datetime(\'now\'),?,?,?,?,?,?,?,?)',(req.lat,req.lon,aqi,temp,hum,wind,text,json.dumps(precautions))); conn.commit(); conn.close()
    return {'risk_level':risk,'advisory_text':text,'precautions':precautions,'aqi':aqi,'temperature':temp,'humidity':hum,'wind_speed':wind}
