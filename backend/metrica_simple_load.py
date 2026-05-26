import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
from datetime import datetime, timedelta
import sys

# 1. ОПРЕДЕЛЯЕМ ПУТИ
current_dir = Path(__file__).resolve().parent
base_dir = current_dir.parent
env_path = base_dir / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Файл .env найден")
else:
    print(f"❌ Файл .env НЕ НАЙДЕН")

# 2. СОБИРАЕМ СТРОКУ ПОДКЛЮЧЕНИЯ
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")
ENV_URL = os.getenv("DATABASE_URL")

if DB_USER and DB_PASS:
    FINAL_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
elif ENV_URL:
    FINAL_URL = ENV_URL
else:
    FINAL_URL = "sqlite:///./gachapets.db"

try:
    engine = create_engine(FINAL_URL)
    with engine.connect() as conn:
        print("🔗 Связь с базой данных установлена!")
except Exception as e:
    print(f"❌ Ошибка подключения к базе: {e}")
    sys.exit(1)

# 3. НАСТРОЙКИ ЯНДЕКСА
TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"

def fetch_metrica():
    if not TOKEN:
        print("❌ Ошибка: YANDEX_METRICA_TOKEN не найден в .env")
        return

    date_today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    url = "https://api-metrika.yandex.net/stat/v1/data"
    
    # dimensions — ровно 10 (максимум)
    dimensions = [
        "ym:s:visitID",            # 0
        "ym:s:dateTime",           # 1
        "ym:s:clientID",           # 2
        "ym:s:paramsLevel1",       # 3
        "ym:s:paramsLevel2",       # 4
        "ym:s:regionCity",         # 5
        "ym:s:deviceCategory",     # 6
        "ym:s:operatingSystemRoot",# 7
        "ym:s:lastTrafficSource",  # 8
        "ym:s:referer"             # 9
    ]
    
    # Метрики — исправленные названия для API Отчетов
    metrics = [
        "ym:s:avgVisitDurationSeconds", # Продолжительность
        "ym:s:pageviews",               # Просмотры (все маленькие!)
        "ym:s:bounceRate"               # Показатель отказов
    ]

    params = {
        "ids": COUNTER_ID,
        "date1": date_start,
        "date2": date_today,
        "accuracy": "full",
        "dimensions": ",".join(dimensions),
        "metrics": ",".join(metrics),
        "limit": 10000
    }
    
    headers = {"Authorization": f"OAuth {TOKEN}"}
    
    print(f"📡 Запрашиваю данные у Яндекса...")
    
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
        
        # Вытаскиваем наш userID
        u_uuid = None
        if dims[3]['name'] == 'userID':
            u_uuid = dims[4]['name']

        rows.append({
            "visit_id": dims[0]['name'],
            "start_time": dims[1]['name'],
            "client_id": dims[2]['name'],
            "user_uuid": u_uuid,
            "city": dims[5]['name'],
            "device": dims[6]['name'],
            "os": dims[7]['name'],
            "source": dims[8]['name'],
            "referrer": dims[9]['name'],
            "visit_duration": int(metr[0]),
            "page_views": int(metr[1]),
            "is_bounce": metr[2] > 0 # Если bounceRate > 0, считаем как отказ
        })

    df = pd.DataFrame(rows)
    
    if not df.empty:
        # Записываем в metrica_logs
        # Используем replace, чтобы всегда иметь свежие данные за 7 дней без дублей
        df.to_sql('metrica_logs', engine, if_exists='replace', index=False)
        print(f"✅ Успешно загружено {len(df)} визитов!")
    else:
        print("📭 Данных от Яндекса пока нет. Нужно подождать ~60 мин после заходов на сайт.")

if __name__ == "__main__":
    fetch_metrica()