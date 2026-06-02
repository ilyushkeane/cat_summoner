from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

# Импортируем нашу модульную систему бэкенда
from backend.database import SessionLocal, engine, Base
from backend.models import User, Summon, UIEvent, MetricaLog

# Автоматически создаем/обновляем таблицы в PostgreSQL при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gachapets API Pro")

# Настройка CORS для работы фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ПУТИ И СТАТИКА ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/style", StaticFiles(directory=os.path.join(BASE_DIR, "style")), name="style")
app.mount("/frontend", StaticFiles(directory=os.path.join(BASE_DIR, "frontend")), name="frontend")

# --- СХЕМЫ ДАННЫХ (Pydantic) ---
class SummonData(BaseModel):
    user_uuid: str
    session_id: str
    cat_title: str
    rarity: str
    referrer: Optional[str] = "direct"
    user_agent: Optional[str] = None
    is_mobile: Optional[bool] = False

class EventData(BaseModel):
    user_uuid: str
    session_id: str
    event_name: str

# --- ЗАВИСИМОСТИ ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ВСПОМОГАТЕЛЬНАЯ ЛОГИКА ---
def get_or_create_user(db: Session, user_uuid: str, metadata: Optional[SummonData] = None):
    """Проверяет наличие юзера и создает его, если он зашел впервые"""
    user = db.query(User).filter(User.user_uuid == user_uuid).first()
    if not user:
        user = User(
            user_uuid=user_uuid,
            referrer=metadata.referrer if metadata else "direct",
            user_agent=metadata.user_agent if metadata else None,
            is_mobile=metadata.is_mobile if metadata else False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"👤 Новый пользователь создан: {user_uuid}")
    return user

# --- ЭНДПОИНТЫ ВЫДАЧИ ФАЙЛОВ ---
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, 'index.html'))

@app.get("/app.js")
async def read_app_js():
    return FileResponse(os.path.join(BASE_DIR, 'app.js'))

# --- API ЭНДПОИНТЫ ---

@app.post("/api/log")
async def log_summon(data: SummonData, db: Session = Depends(get_db)):
    """Логирует призыв кота и привязывает его к пользователю и сессии"""
    try:
        # Убеждаемся, что юзер существует
        get_or_create_user(db, data.user_uuid, data)
        
        # Создаем запись о призыве
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/event")
async def log_ui_event(data: EventData, db: Session = Depends(get_db)):
    """Логирует действия в интерфейсе (открытие меню и т.д.)"""
    try:
        # Убеждаемся, что юзер существует (мог нажать инфо до первого призыва)
        get_or_create_user(db, data.user_uuid)
        
        new_event = UIEvent(
            user_uuid=data.user_uuid,
            session_id=data.session_id,
            event_name=data.event_name
        )
        db.add(new_event)
        db.commit()
        return {"status": "success", "message": "Event logged"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_cat/{tag}")
async def get_local_cat(tag: str):
    """Выдает случайную картинку из папки тега"""
    cat_path = os.path.join(BASE_DIR, "static", "cats", tag)
    
    # Если папки нет — фоллбек на случайную
    if not os.path.exists(cat_path) or not os.listdir(cat_path):
        cats_root = os.path.join(BASE_DIR, "static", "cats")
        all_tags = [d for d in os.listdir(cats_root) if os.path.isdir(os.path.join(cats_root, d))]
        cat_path = os.path.join(cats_root, random.choice(all_tags))

    files = [f for f in os.listdir(cat_path) if f.endswith(('.jpg', '.png', '.jpeg', '.webp'))]
    if not files:
        raise HTTPException(status_code=404, detail="No images found")
        
    return FileResponse(os.path.join(cat_path, random.choice(files)))

# Эндпоинт для быстрой проверки базы (опционально)
@app.get("/api/debug/users")
def get_users_debug(db: Session = Depends(get_db)):
    return db.query(User).limit(10).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)