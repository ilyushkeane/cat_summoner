import os
import random
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models import Summon
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Раздача статики
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/style", StaticFiles(directory=os.path.join(BASE_DIR, "style")), name="style")
app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="frontend")

class SummonData(BaseModel):
    user_uuid: str
    cat_title: str
    rarity: str

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/")
async def read_index(): return FileResponse('index.html')

@app.get("/app.js")
async def get_app_js():
    return FileResponse(os.path.join(BASE_DIR, 'app.js'), media_type='application/javascript')

@app.post("/api/log")
async def log_click(data: SummonData, db: Session = Depends(get_db)):
    new_entry = Summon(user_uuid=data.user_uuid, cat_title=data.cat_title, rarity=data.rarity)
    db.add(new_entry)
    db.commit()
    return {"status": "success"}

@app.get("/api/get_cat/{tag}")
async def get_local_cat(tag: str):
    cat_path = os.path.join(BASE_DIR, "static", "cats", tag)
    if not os.path.exists(cat_path) or not os.listdir(cat_path):
        tag = random.choice(os.listdir(os.path.join(BASE_DIR, "static", "cats")))
        cat_path = os.path.join(BASE_DIR, "static", "cats", tag)
    
    files = [f for f in os.listdir(cat_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    return FileResponse(os.path.join(cat_path, random.choice(files)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)