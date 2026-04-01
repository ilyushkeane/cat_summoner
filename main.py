import os
import random
import uvicorn
from urllib.parse import quote_plus
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Загружаем настройки из .env
load_dotenv()

# --- 1. НАСТРОЙКИ ПУТЕЙ (Обязательно должны быть здесь) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATS_DIR = os.path.join(BASE_DIR, "static", "cats")

# --- 2. СБОРКА DATABASE_URL ---
# Пытаемся собрать URL из кирпичиков (это самый безопасный метод для Windows)
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")

if DB_USER and DB_PASS:
    # Если есть логин и пароль, собираем PostgreSQL URL с экранированием
    DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
else:
    # Если кирпичиков нет, берем готовую строку из .env или используем SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gachapets.db")

# --- 3. СОЗДАНИЕ ENGINE ---
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Для PostgreSQL добавляем явное указание кодировки (помогает от UnicodeDecodeError)
    engine = create_engine(DATABASE_URL, client_encoding='utf8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 4. МОДЕЛЬ БД ---
class Summon(Base):
    __tablename__ = "summons"
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(String)
    cat_title = Column(String)
    rarity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- 5. ПРИЛОЖЕНИЕ ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Проверяем и создаем папку со статикой
if not os.path.exists(CATS_DIR):
    os.makedirs(CATS_DIR)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class SummonData(BaseModel):
    user_uuid: str
    cat_title: str
    rarity: str

# --- 6. ЭНДПОИНТЫ ---

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

@app.get("/api/all")
def get_all_summons():
    db = SessionLocal()
    try:
        return db.query(Summon).all()
    finally:
        db.close()

@app.get("/api/get_cat/{tag}")
async def get_local_cat(tag: str):
    tag_path = os.path.join(CATS_DIR, tag)
    
    if not os.path.exists(tag_path) or not os.listdir(tag_path):
        all_tags = [d for d in os.listdir(CATS_DIR) if os.path.isdir(os.path.join(CATS_DIR, d))]
        if not all_tags: raise HTTPException(status_code=404, detail="Нет папок с котами")
        tag_path = os.path.join(CATS_DIR, random.choice(all_tags))

    files = [f for f in os.listdir(tag_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    random_cat = random.choice(files)
    return FileResponse(os.path.join(tag_path, random_cat))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)