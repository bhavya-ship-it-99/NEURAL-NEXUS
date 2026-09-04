from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import init_db
from .routers import weather, forecast, aqi, profile, advisory, alerts, history
init_db()
app=FastAPI(title='AeroCare')
app.include_router(weather.router,prefix='/api/weather',tags=['weather'])
app.include_router(forecast.router,prefix='/api/forecast',tags=['forecast'])
app.include_router(aqi.router,prefix='/api/aqi',tags=['aqi'])
app.include_router(profile.router,prefix='/api/profile',tags=['profile'])
app.include_router(advisory.router,prefix='/api/advisory',tags=['advisory'])
app.include_router(alerts.router,prefix='/api/alerts',tags=['alerts'])
app.include_router(history.router,prefix='/api/history',tags=['history'])
frontend_path=Path(__file__).parent.parent/'frontend'
app.mount('/',StaticFiles(directory=frontend_path,html=True),name='frontend')
