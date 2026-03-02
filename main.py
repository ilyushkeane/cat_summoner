import os
import random
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- ПУТИ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATS_DIR = os.path.join(BASE_DIR, "static", "cats")

# --- БАЗА ДАННЫХ ---
DATABASE_URL = "sqlite:///./gachapets.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Summon(Base):
    __tablename__ = "summons"
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String)
    cat_title = Column(String)
    rarity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- APP ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статику, чтобы картинки были доступны по прямым ссылкам
if not os.path.exists(CATS_DIR):
    os.makedirs(CATS_DIR)
app.mount("/static", StaticFiles(directory="static"), name="static")

class SummonData(BaseModel):
    user_uuid: str
    cat_title: str
    rarity: str

# Эндпоинт 1: Запись в базу
@app.post("/api/log")
async def log_click(data: SummonData):
    db = SessionLocal()
    try:
        new_entry = Summon(user_uuid=data.user_uuid, cat_title=data.cat_title, rarity=data.rarity)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        print(f"✅ Запись создана: ID {new_entry.id} | {data.cat_title}")
        return {"status": "success", "id": new_entry.id}
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка БД: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")
    finally:
        db.close()

# Эндпоинт для просмотра всех записей в базе
@app.get("/api/all")
def get_all_summons():
    db = SessionLocal()
    try:
        # Запрашиваем все записи из таблицы Summon
        summons = db.query(Summon).all()
        return summons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Эндпоинт 2: Случайная картинка по тегу
@app.get("/api/get_cat/{tag}")
async def get_local_cat(tag: str):
    tag_path = os.path.join(CATS_DIR, tag)
    if not os.path.exists(tag_path) or not os.listdir(tag_path):
        # Если папки нет, берем из первой попавшейся
        all_tags = [d for d in os.listdir(CATS_DIR) if os.path.isdir(os.path.join(CATS_DIR, d))]
        if not all_tags: raise HTTPException(status_code=404, detail="Нет папок с котами")
        tag_path = os.path.join(CATS_DIR, random.choice(all_tags))

    files = [f for f in os.listdir(tag_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    random_cat = random.choice(files)
    return FileResponse(os.path.join(tag_path, random_cat))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)