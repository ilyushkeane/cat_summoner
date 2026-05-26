import os
import requests
import pandas as pd
import base64
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Настройки (убедись, что они есть в .env)
TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"
engine = create_engine(os.getenv("DATABASE_URL"))

def decode_uuid(val):
    """Простое декодирование нашего userID из params64"""
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