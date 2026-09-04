import json
from fastapi import APIRouter
from ..database import get_connection
router=APIRouter()
@router.get('/')
def history():
    c=get_connection(); rows=c.execute('SELECT * FROM advisory_history ORDER BY id DESC LIMIT 30').fetchall(); c.close(); return {'history':[{'timestamp':r['timestamp'],'aqi':r['aqi'],'temp':r['temp'],'advisory_text':r['advisory_text'],'precautions':json.loads(r['precautions'] or '[]')} for r in rows]}
