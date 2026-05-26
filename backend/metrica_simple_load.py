import os
import requests
import pandas as pd
import time
import io
import base64
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
from datetime import datetime, timedelta
import sys

# 1. НАСТРОЙКИ ПУТЕЙ И .ENV
current_dir = Path(__file__).resolve().parent
base_dir = current_dir.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

# 2. ПОДКЛЮЧЕНИЕ К БАЗЕ
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")
FINAL_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
engine = create_engine(FINAL_URL)

# 3. НАСТРОЙКИ ЯНДЕКСА
TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"
HEADERS = {"Authorization": f"OAuth {TOKEN}"}

# Список полей, которые разрешены в Logs API
FIELDS = [
    "ym:s:visitID", "ym:s:dateTime", "ym:s:clientID", "ym:s:regionCity",
    "ym:s:deviceCategory", "ym:s:operatingSystemRoot", "ym:s:lastTrafficSource",
    "ym:s:referer", "ym:s:params64", "ym:s:visitDuration", "ym:s:pageViews", "ym:s:isBounce"
]

def decode_uuid(val):
    try:
        if not val or val == "" or val == "[]": return None
        decoded = base64.b64decode(val).decode('utf-8')
        return json.loads(decoded).get('userID')
    except:
        return None

def run_logs_api():
    if not TOKEN:
        print("❌ Ошибка: Токен не найден")
        return

    # Берем данные за вчера и сегодня
    date_start = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    date_end = datetime.now().strftime('%Y-%m-%d')

    log_url = f"https://api-metrika.yandex.net/management/v1/counter/{COUNTER_ID}/logrequests"
    
    # А. СОЗДАЕМ ЗАПРОС
    print(f"📡 Создаю запрос на логи за {date_start} - {date_end}...")
    params = {
        "date1": date_start,
        "date2": date_end,
        "fields": ",".join(FIELDS),
        "source": "visits"
    }
    
    res = requests.post(log_url, params=params, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Ошибка создания: {res.text}")
        return
    
    request_id = res.json()['log_request']['request_id']
    print(f"✅ Запрос {request_id} принят. Яндекс начал сборку файлов...")

    # Б. ЖДЕМ ГОТОВНОСТИ (Цикл ожидания)
    while True:
        status_res = requests.get(f"{log_url}/{request_id}", headers=HEADERS)
        status = status_res.json()['log_request']['status']
        print(f"⌛ Статус сборки: {status}")
        
        if status == 'processed': break
        if status in ['error', 'cleaned_by_user']:
            print("❌ Ошибка при сборке логов на стороне Яндекса.")
            return
        time.sleep(15) # Ждем 15 секунд перед следующей проверкой

    # В. СКАЧИВАЕМ И СОХРАНЯЕМ
    parts = status_res.json()['log_request']['parts']
    all_dfs = []

    for part in parts:
        part_num = part['part_number']
        print(f"📥 Скачиваю часть {part_num}...")
        down_url = f"{log_url}/{request_id}/part/{part_num}/download"
        data_res = requests.get(down_url, headers=HEADERS)
        
        df_part = pd.read_csv(io.StringIO(data_res.text), sep="\t")
        all_dfs.append(df_part)

    if all_dfs:
        df = pd.concat(all_dfs)
        
        # Г. ТРАНСФОРМАЦИЯ (Декодируем UUID и переименовываем)
        df['user_uuid'] = df['ym:s:params64'].apply(decode_uuid)
        
        final_df = pd.DataFrame({
            "visit_id": df['ym:s:visitID'].astype(str),
            "start_time": pd.to_datetime(df['ym:s:dateTime']),
            "client_id": df['ym:s:clientID'].astype(str),
            "user_uuid": df['user_uuid'],
            "city": df['ym:s:regionCity'],
            "device": df['ym:s:deviceCategory'],
            "os": df['ym:s:operatingSystemRoot'],
            "source": df['ym:s:lastTrafficSource'],
            "referrer": df['ym:s:referer'],
            "visit_duration": df['ym:s:visitDuration'].astype(int),
            "page_views": df['ym:s:pageViews'].astype(int),
            "is_bounce": df['ym:s:isBounce'].astype(int) == 1
        })

        # Записываем в базу
        final_df.to_sql('metrica_logs', engine, if_exists='replace', index=False)
        print(f"🎉 ФИНИШ! Загружено {len(final_df)} уникальных визитов.")

        # Очищаем за собой в Яндексе
        requests.post(f"{log_url}/{request_id}/clean", headers=HEADERS)
    else:
        print("📭 Данных не обнаружено.")

if __name__ == "__main__":
    run_logs_api()