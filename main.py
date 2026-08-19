import os
import random
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Импорты из твоих модулей
from backend.database import SessionLocal, engine, Base
from backend.models import User, Summon, UIEvent, MetricaLog

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gachapets API Pro - Protected Edition")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- СПИСКИ РАЗРЕШЕННЫХ ЗНАЧЕНИЙ (White Lists) ---
ALLOWED_CATS = {
    "Картонный Барон", "Мастер Хлебушек", "Инспектор Пола", "Белое Облачко",
    "Теневой Ниндзя", "Загадочный Философ", "Вечный Котёнок", "Рыжая Улыбка",
    "Инструктор Йоги", "Офисный Планктон", "Генеральный Директор", "Профессор Мяу",
    "Олимпийский Прыгун", "Оперная Дива", "Пищевой Критик", "Ночной Тыгыдык",
    "Кото-Пират", "Супер-Кот", "Пчело-Кот", "Властелин Прайда", "Гроза Джунглей",
    "Акула-Кот", "Кото-Завр"
}

ALLOWED_RARITIES = {"common", "rare", "epic", "legendary"}

ALLOWED_EVENTS = {"app_init", "summon_attempt", "cat_summon_success", "open_info", "legendary_drop", "technical_error"}

# --- СХЕМЫ ДАННЫХ С ВАЛИДАЦИЕЙ ---

class SummonData(BaseModel):
    # Ограничиваем длину строк, чтобы боты не слали гигабайты текста
    user_uuid: str = Field(..., min_length=5, max_length=100)
    session_id: str = Field(..., min_length=5, max_length=100)
    cat_title: str = Field(..., max_length=100)
    rarity: str = Field(..., max_length=20)
    referrer: Optional[str] = Field("direct", max_length=255)
    user_agent: Optional[str] = Field(None, max_length=500)
    is_mobile: Optional[bool] = False

    @field_validator('cat_title')
    @classmethod
    def check_cat_title(cls, v):
        if v not in ALLOWED_CATS:
            raise ValueError('Invalid cat title')
        return v

    @field_validator('rarity')
    @classmethod
    def check_rarity(cls, v):
        if v not in ALLOWED_RARITIES:
            raise ValueError('Invalid rarity class')
        return v

class EventData(BaseModel):
    user_uuid: str = Field(..., max_length=100)
    session_id: str = Field(..., max_length=100)
    event_name: str = Field(..., max_length=50)

    @field_validator('event_name')
    @classmethod
    def check_event_name(cls, v):
        if v not in ALLOWED_EVENTS:
            raise ValueError('Unknown event')
        return v

# --- ЗАВИСИМОСТИ ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(db: Session, user_uuid: str, metadata: Optional[SummonData] = None):
    user = db.query(User).filter(User.user_uuid == user_uuid).first()
    if not user:
        # Если юзера нет, создаем его, обрезая возможный спам в метаданных
        user = User(
            user_uuid=user_uuid,
            referrer=(metadata.referrer[:250] if metadata and metadata.referrer else "direct"),
            user_agent=(metadata.user_agent[:450] if metadata and metadata.user_agent else None),
            is_mobile=(metadata.is_mobile if metadata else False)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# --- МАРШРУТЫ ---

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/app.js")
async def read_app_js():
    return FileResponse('app.js')

@app.mount("/static", StaticFiles(directory="static"), name="static")
@app.mount("/style", StaticFiles(directory="style"), name="style")
@app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.post("/api/log")
async def log_summon(data: SummonData, db: Session = Depends(get_db)):
    try:
        get_or_create_user(db, data.user_uuid, data)
        
        new_summon = Summon(
            user_uuid=data.user_uuid,
            session_id=data.session_id,
            cat_title=data.cat_title,
            rarity=data.rarity
        )
        db.add(new_summon)
        db.commit()
        return {"status": "success", "message": "Summon logged"}
    except Exception as e:
        db.rollback()
        # Мы не отдаем детали ошибки наружу (security), просто 400
        raise HTTPException(status_code=400, detail="Data validation failed")

@app.post("/api/event")
async def log_ui_event(data: EventData, db: Session = Depends(get_db)):
    try:
        get_or_create_user(db, data.user_uuid)
        
        new_event = UIEvent(
            user_uuid=data.user_uuid,
            session_id=data.session_id,
            event_name=data.event_name
        )
        db.add(new_event)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid event data")

@app.get("/api/get_cat/{tag}")
async def get_local_cat(tag: str):
    # Очищаем tag от возможных спецсимволов для безопасности
    safe_tag = "".join(x for x in tag if x.isalnum() or x == "-")
    cat_path = os.path.join("static", "cats", safe_tag)
    
    if not os.path.exists(cat_path) or not os.listdir(cat_path):
        return HTTPException(status_code=404)

    files = [f for f in os.listdir(cat_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    return FileResponse(os.path.join(cat_path, random.choice(files)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)