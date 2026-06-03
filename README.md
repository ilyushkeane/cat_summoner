# 🐾 Gachapets: Fullstack Analytics & Gacha System

<p align="center">
  <img src="img/preview.png" alt="Gachapets Preview" width="600">
</p>

<p align="center">
  <a href="https://gachapets.ru"><strong>🚀 Live Demo</strong></a> | 
  <a href="https://datalens.yandex/m3m1tdjsuzx86"><strong>📊 Live BI Dashboard</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Production-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Data--Driven-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/JavaScript-Modular%20ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/DevOps-Nginx%20%7C%20SSL-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx">
</p>

---

## 🌟 О проекте

**Gachapets** — это интерактивная Fullstack-платформа, объединяющая игровую механику "Гача" с профессиональной системой сквозной аналитики. Проект демонстрирует полный цикл разработки: от создания модульного фронтенда до настройки ETL-пайплайнов и построения BI-дашбордов.

### 🎯 Ключевые фичи
- **Smart Pity System:** Алгоритм "защиты от неудач" — гарантированный легендарный дроп на 20-й призыв внутри сессии.
- **End-to-End Analytics:** Сквозная связка данных из PostgreSQL и Yandex.Metrica API по уникальному `user_uuid`.
- **Traffic Attribution:** Система отслеживания источников трафика через кастомные URL-метки (`?ref=tg`) с записью в БД.
- **Automated ETL:** Python-скрипты на базе `Pandas` для ежедневной выгрузки, дедупликации и сессионизации данных по расписанию (Cron).
- **High-Performance Static:** Оптимизированная раздача медиа-контента напрямую через Nginx.

---

## 🏗 Архитектура системы

```mermaid
graph TD
    User((Пользователь)) -->|HTTPS / 443| Nginx{Nginx Proxy}
    
    subgraph "Frontend (Modular ES6)"
        Nginx -->|Static Content| HTML[index.html / CSS]
        HTML -->|Logic| JS[app.js / modules]
        JS -->|Tracking| YM[Yandex Metrika / GA4]
    end

    subgraph "Backend (FastAPI Server)"
        Nginx -->|API Proxy| FastAPI[FastAPI App]
        FastAPI -->|ORM SQLAlchemy| DB[(PostgreSQL)]
        Nginx -->|Local Storage| Disk[Cat Image Archive]
    end

    subgraph "BI & Data Engineering"
        DB -->|ETL Script| Python[metrica_simple_load.py]
        Python -->|API Request| YM
        DB -->|Connector| DataLens[Yandex DataLens BI]
    end
```

erDiagram
    USERS ||--o{ SUMMONS : "performs"
    USERS ||--o{ UI_EVENTS : "triggers"

    USERS {
        string user_uuid PK "Unique Identity"
        datetime first_seen "Registration Date"
        string referrer "Source (tg, direct, etc)"
        boolean is_mobile "Device Type"
    }

    SUMMONS {
        int id PK
        string user_uuid FK "User Link"
        string session_id "Session tracking"
        string cat_title "Character Name"
        string rarity "Tier"
        datetime timestamp "Event Time"
    }

    UI_EVENTS {
        int id PK
        string user_uuid FK "User Link"
        string event_name "Action (open_info, etc)"
        datetime timestamp "Event Time"
    }
