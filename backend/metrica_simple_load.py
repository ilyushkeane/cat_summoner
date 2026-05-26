import os
import requests
import pandas as pd
import base64
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
import sys

# 1. ОПРЕДЕЛЯЕМ ПУТИ
# Находим папку, где лежит этот файл (backend)
current_dir = Path(__file__).resolve().parent
# Находим корень проекта (на уровень выше)
base_dir = current_dir.parent
# Путь к .env
env_path = base_dir / '.env'

# Загружаем переменные из .env
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Файл .env найден по адресу: {env_path}")
else:
    print(f"❌ Файл .env НЕ НАЙДЕН по адресу: {env_path}")

# 2. СОБИРАЕМ СТРОКУ ПОДКЛЮЧЕНИЯ (как в main.py)
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")
ENV_URL = os.getenv("DATABASE_URL")

# Логика выбора URL
if DB_USER and DB_PASS:
    # Если есть логин и пароль, собираем Postgres URL (самый надежный вариант)
    FINAL_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
    print(f"📡 Сборка URL из компонентов: {DB_USER}@localhost/{DB_NAME}")
elif ENV_URL:
    # Если в .env прописана готовая строка DATABASE_URL
    FINAL_URL = ENV_URL
    print(f"📡 Использование готового DATABASE_URL из .env")
else:
    # Если ничего не нашли — фоллбек на локальный sqlite, чтобы скрипт не упал
    FINAL_URL = "sqlite:///./gachapets.db"
    print("🏠 Переменные БД не найдены, использую SQLite по умолчанию.")

# Создаем движок SQLAlchemy
try:
    engine = create_engine(FINAL_URL)
    # Тестовое подключение
    with engine.connect() as conn:
        print("🔗 Связь с базой данных установлена успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения к базе: {e}")
    sys.exit(1)

# 3. НАСТРОЙКИ ЯНДЕКСА
TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"

def decode_uuid(val):
    try:
        if not val or val == "": return None
        decoded = base64.b64decode(val).decode('utf-8')
        return json.loads(decoded).get('userID')
    except:
        return None

def fetch_metrica():
    if not TOKEN:
        print("❌ Ошибка: YANDEX_METRICA_TOKEN не найден в .env")
        return

    url = "https://api-metrika.yandex.net/stat/v1/data"
    
    # Мы оставили ровно 10 самых важных полей (это лимит API)
    dimensions = [
        "ym:s:visitID",            # 1
        "ym:s:dateTime",           # 2
        "ym:s:clientID",           # 3
        "ym:s:params64",           # 4 (наш user_uuid)
        "ym:s:regionCity",         # 5
        "ym:s:deviceCategory",     # 6
        "ym:s:operatingSystemRoot",# 7
        "ym:s:lastTrafficSource",  # 8
        "ym:s:referer",            # 9
        "ym:s:lastUTMSource"       # 10
    ]
    
    metrics = [
        "ym:s:visitDuration",
        "ym:s:pageViews",
        "ym:s:isBounce"
    ]

    params = {
        "ids": COUNTER_ID,
        "date1": "7daysago",
        "date2": "today",
        "accuracy": "full",
        "dimensions": ",".join(dimensions),
        "metrics": ",".join(metrics),
        "limit": 10000
    }
    
    headers = {"Authorization": f"OAuth {TOKEN}"}
    
    print("📡 Запрашиваю данные у Яндекса (оптимизированный список)...")
    try:
        res = requests.get(url, params=params, headers=headers)
        if res.status_code != 200:
            print(f"❌ Ошибка Яндекса: {res.status_code}")
            print(f"Текст ошибки: {res.text}")
            return
        data = res.json()['data']
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return
    
    rows = []
    for item in data:
        dims = item['dimensions']
        metr = item['metrics']
        # Наполняем данными согласно новому порядку (dimensions)
        rows.append({
            "visit_id": dims[0]['name'],
            "start_time": dims[1]['name'],
            "client_id": dims[2]['name'],
            "user_uuid": decode_uuid(dims[3]['name']),
            "city": dims[4]['name'],
            "device": dims[5]['name'],
            "os": dims[6]['name'],
            "source": dims[7]['name'],
            "referrer": dims[8]['name'],
            "utm_source": dims[9]['name'],
            "visit_duration": int(metr[0]),
            "page_views": int(metr[1]),
            "is_bounce": bool(metr[2])
        })

    df = pd.DataFrame(rows)
    
    if not df.empty:
        # ВАЖНО: Мы удалили некоторые поля из запроса, 
        # поэтому в БД в этих колонках (country, region и т.д.) будет NULL.
        # Это нормально для текущего этапа.
        df.to_sql('metrica_logs', engine, if_exists='replace', index=False)
        print(f"✅ Успешно загружено {len(df)} визитов в таблицу metrica_logs")
    else:
        print("📭 Данных от Яндекса пока нет. Проверь счетчик и были ли заходы на сайт.")
        
if __name__ == "__main__":
    fetch_metrica()