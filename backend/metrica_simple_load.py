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
    url = "https://api-metrika.yandex.net/stat/v1/data"
    
    # Список полей (Dimensions - характеристики, Metrics - цифры)
    params = {
        "ids": COUNTER_ID,
        "date1": "7daysago", # За какой период берем
        "date2": "today",
        "accuracy": "full",
        "dimensions": (
            "ym:s:visitID,ym:s:dateTime,ym:s:clientID,ym:s:params64,"
            "ym:s:regionCountry,ym:s:regionArea,ym:s:regionCity,"
            "ym:s:deviceCategory,ym:s:operatingSystemRoot,ym:s:browser,"
            "ym:s:lastTrafficSource,ym:s:lastUTMSource,ym:s:lastUTMMedium,ym:s:lastUTMCampaign,ym:s:referer"
        ),
        "metrics": "ym:s:visitDuration,ym:s:pageViews,ym:s:isBounce",
        "limit": 10000 # Сколько визитов за раз (макс 100к), сейчас 10к
    }
    
    headers = {"Authorization": f"OAuth {TOKEN}"}
    
    print("📡 Запрашиваю данные у Яндекса...")
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    data = res.json()['data']
    
    # Превращаем сложный JSON Яндекса в плоский список
    rows = []
    for item in data:
        dims = item['dimensions']
        metr = item['metrics']
        rows.append({
            "visit_id": dims[0]['name'],
            "start_time": dims[1]['name'],
            "client_id": dims[2]['name'],
            "user_uuid": decode_uuid(dims[3]['name']),
            "country": dims[4]['name'],
            "region": dims[5]['name'],
            "city": dims[6]['name'],
            "device": dims[7]['name'],
            "os": dims[8]['name'],
            "browser": dims[9]['name'],
            "source": dims[10]['name'],
            "utm_source": dims[11]['name'],
            "utm_medium": dims[12]['name'],
            "utm_campaign": dims[13]['name'],
            "referrer": dims[14]['name'],
            "visit_duration": int(metr[0]),
            "page_views": int(metr[1]),
            "is_bounce": bool(metr[2])
        })

    # Загружаем в Pandas и в базу
    df = pd.DataFrame(rows)
    
    if not df.empty:
        # if_exists='append' добавит новые, но может дублировать. 
        # На простом уровне это ок, потом можно чистить дубли в SQL.
        df.to_sql('metrica_logs', engine, if_exists='replace', index=False)
        print(f"✅ Успешно загружено {len(df)} визитов в таблицу metrica_logs")
    else:
        print("📭 Данных за этот период нет.")

if __name__ == "__main__":
    fetch_metrica()