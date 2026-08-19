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

def generate_id(time_str, client_id):
    seed = f"{time_str}{client_id}"
    return hashlib.md5(seed.encode()).hexdigest()[:16]

def fetch_metrica_final_fixed():
    if not TOKEN:
        print("❌ Ошибка: Токен не найден")
        return

    url = "https://api-metrika.yandex.net/stat/v1/data"
    date_today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    params = {
        "ids": COUNTER_ID,
        "date1": date_start,
        "date2": date_today,
        "accuracy": "full",
        "dimensions": "ym:s:dateTime,ym:s:paramsLevel1,ym:s:paramsLevel2,ym:s:regionCity,ym:s:deviceCategory,ym:s:operatingSystemRoot,ym:s:lastTrafficSource,ym:s:referer,ym:s:clientID",
        "metrics": "ym:s:visits,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds",
        "limit": 10000
    }
    
    headers = {"Authorization": f"OAuth {TOKEN}"}
    print(f"📡 Запрашиваю данные (период {date_start} - {date_today})...")
    
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json().get('data', [])
    
    rows = []
    found_keys = set() # Для отладки

    for item in data:
        d = [x['name'] for x in item['dimensions']]
        m = item['metrics']
        
        param_name = str(d[1]) if d[1] else ""
        param_value = str(d[2]) if d[2] else None
        
        if param_name:
            found_keys.add(param_name)

        # ПРОВЕРКА КЛЮЧА: ищем user_id или userID (регистр не важен)
        u_uuid = None
        if param_name.lower() in ['user_id', 'userid']:
            u_uuid = param_value.strip() if param_value else None
        
        rows.append({
            "temp_id": generate_id(d[0], d[8]),
            "start_time": pd.to_datetime(d[0]),
            "user_uuid": u_uuid, 
            "city": d[3],
            "device": d[4],
            "os": d[5],
            "source": d[6],
            "referrer": d[7],
            "client_id": d[8],
            "visits": int(m[0]),
            "pageviews": int(m[1]),
            "bounce_rate": float(m[2]),
            "duration": int(m[3])
        })

    raw_df = pd.DataFrame(rows)
    print(f"🔍 Найденные ключи параметров в Яндексе: {list(found_keys)}")

    if raw_df.empty:
        print("📭 Данных нет.")
        return

    # Схлопываем дубликаты визитов, приоритет строкам с UUID
    df_sorted = raw_df.sort_values(by=['temp_id', 'user_uuid'], ascending=[True, False])
    df_final = df_sorted.drop_duplicates(subset=['temp_id'], keep='first').copy()
    df_final['visit_id'] = df_final['temp_id']
    df_final = df_final.drop(columns=['temp_id'])

    df_final.to_sql('yandex_metrica_data', engine, if_exists='replace', index=False)
    
    count_with_id = df_final['user_uuid'].notnull().sum()
    print(f"✅ Готово! Всего визитов: {len(df_final)}")
    print(f"🔑 Из них с привязанным ID: {count_with_id}")

if __name__ == "__main__":
    fetch_metrica_final_fixed()