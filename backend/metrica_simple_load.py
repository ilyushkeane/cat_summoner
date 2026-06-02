import os
import requests
import pandas as pd
import hashlib
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
from datetime import datetime, timedelta

# 1. Настройки путей и базы
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=base_dir / '.env')

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")
engine = create_engine(f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}")

TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"

def fetch_and_clean_metrica():
    url = "https://api-metrika.yandex.net/stat/v1/data"
    date_today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    params = {
        "ids": COUNTER_ID,
        "date1": date_start,
        "date2": date_today,
        "accuracy": "full",
        "dimensions": "ym:s:dateTime,ym:s:paramsLevel2,ym:s:regionCity,ym:s:deviceCategory,ym:s:operatingSystemRoot,ym:s:lastTrafficSource,ym:s:referer,ym:s:clientID",
        "metrics": "ym:s:visits,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds",
        "limit": 10000,
        "filters": "ym:s:paramsLevel1=='userID'"
    }
    
    headers = {"Authorization": f"OAuth {TOKEN}"}
    
    print("📡 Запрашиваю чистые данные у Яндекса...")
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json()['data']
    
    rows = []
    for item in data:
        d = [x['name'] for x in item['dimensions']]
        m = item['metrics']
        
        # Генерация уникального ID
        visit_hash = hashlib.md5(f"{d[0]}{d[1]}".encode()).hexdigest()[:16]
        
        rows.append({
            "visit_id": visit_hash,
            "date_time": pd.to_datetime(d[0]),
            "user_uuid": str(d[1]).strip(), # УБИРАЕМ ПРОБЕЛЫ
            "city": str(d[2]).strip(),
            "device": str(d[3]).strip(),
            "os": str(d[4]).strip(),
            "source": str(d[5]).strip(),
            "referrer": str(d[6]).strip(),
            "client_id": str(d[7]).strip(), # УБИРАЕМ ПРОБЕЛЫ
            "visits": int(m[0]),
            "pageviews": int(m[1]),
            "bounce_rate": float(m[2]),
            "duration": int(m[3])
        })

    df = pd.DataFrame(rows)
    
    if not df.empty:
        # replace создаст таблицу с правильными типами данных VARCHAR
        df.to_sql('yandex_metrica_data', engine, if_exists='replace', index=False)
        print(f"✅ Таблица пересоздана! Загружено {len(df)} чистых строк.")
    else:
        print("📭 Нет данных для загрузки.")

if __name__ == "__main__":
    fetch_and_clean_metrica()