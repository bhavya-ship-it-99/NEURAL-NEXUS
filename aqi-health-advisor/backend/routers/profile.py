import json
from fastapi import APIRouter
from ..models import ProfileIn
from ..database import get_connection
router=APIRouter()
@router.get('/')
def get_profile():
    c=get_connection(); row=c.execute('SELECT * FROM profile WHERE id=1').fetchone(); c.close()
    if not row:return {"age_group":"18-39","medical_history":[],"occupation":""}
    return {"age_group":row['age_group'] or '18-39',"medical_history":json.loads(row['medical_history'] or '[]'),"occupation":row['occupation'] or ''}
@router.post('/')
def save_profile(p:ProfileIn):
    c=get_connection(); c.execute('INSERT INTO profile(id,age_group,medical_history,occupation) VALUES(1,?,?,?) ON CONFLICT(id) DO UPDATE SET age_group=excluded.age_group, medical_history=excluded.medical_history, occupation=excluded.occupation',(p.age_group,json.dumps(p.medical_history),p.occupation)); c.commit(); c.close(); return p.model_dump()
