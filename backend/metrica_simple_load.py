import os
import requests
import pandas as pd
import hashlib
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pathlib import Path
from datetime import datetime, timedelta
import sys

# 1. НАСТРОЙКИ ПУТЕЙ
current_dir = Path(__file__).resolve().parent
base_dir = current_dir.parent
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)

# 2. ПОДКЛЮЧЕНИЕ К БАЗЕ
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "gachapets_db")

if DB_USER and DB_PASS:
    FINAL_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
else:
    FINAL_URL = os.getenv("DATABASE_URL", "sqlite:///./gachapets.db")

engine = create_engine(FINAL_URL)

# 3. НАСТРОЙКИ ЯНДЕКСА
TOKEN = os.getenv("YANDEX_METRICA_TOKEN")
COUNTER_ID = "107060992"

def generate_pseudo_id(uuid, time_str):
    """Создает уникальный ID визита, если Яндекс его не отдает"""
    seed = f"{uuid}{time_str}"
    return hashlib.md5(seed.encode()).hexdigest()[:16]

def fetch_metrica():
    if not TOKEN:
        print("❌ Ошибка: Токен не найден в .env")
        return None

    # Берем данные за последние 30 дней
    date_today = datetime.now().strftime('%Y-%m-%d')
    date_start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    url = "https://api-metrika.yandex.net/stat/v1/data"  # Исправлено: https:// → https://

    dimensions = [
        "ym:s:dateTime",
        "ym:s:paramsLevel2",
        "ym:s:regionCity",
        "ym:s:deviceCategory",
        "ym:s:operatingSystemRoot",
        "ym:s:lastTrafficSource",
        "ym:s:referer",
        "ym:s:clientID"
    ]

    metrics = [
        "ym:s:visits",
        "ym:s:pageviews",
        "ym:s:bounceRate",
        "ym:s:avgVisitDurationSeconds"
    ]

    params = {
        "ids": COUNTER_ID,
        "date1": date_start,
        "date2": date_today,  # Исправлено: date_to → date_today
        "metrics": ",".join(metrics),
        "dimensions": ",".join(dimensions),
        "limit": 10000,  # Лимит на запрос
        "oauth_token": TOKEN  # Токен авторизации
    }

    headers = {
        "Authorization": f"OAuth {TOKEN}"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Проверка HTTP-статуса

        data = response.json()

        if 'data' not in data:
            print("⚠️ Предупреждение: В ответе API нет данных")
            return None

        # Преобразование в DataFrame
        rows = []
        for row in data['data']:
            dim_values = [d['name'] for d in row['dimensions']]
            metric_values = row['metrics']
            rows.append(dim_values + metric_values)

        columns = [d.split(':')[-1] for d in dimensions] + [m.split(':')[-1] for m in metrics]
        df = pd.DataFrame(rows, columns=columns)

        # Сохранение в БД
        df.to_sql('yandex_metrica_data', engine, if_exists='append', index=False)
        print(f"✅ Успешно загружено {len(df)} записей")
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса к API: {e}")
        return None
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return None

# Запуск функции
if __name__ == "__main__":
    fetch_metrica()
