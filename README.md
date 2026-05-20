# 🐾 Gachapets: Fullstack Analytics & Gacha System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Production-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Data--Driven-336791?logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/JavaScript-Modular%20ES6-F7DF1E?logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/Infrastructure-Nginx%20%7C%20SSL-009639?logo=nginx&logoColor=white" alt="Nginx">
</p>

**Gachapets** — это высоконагруженное (по архитектуре) Fullstack-приложение, сочетающее игровую механику "Гача" и комплексную систему сбора и анализа пользовательских данных. Проект демонстрирует переход от простых скриптов к масштабируемой модульной архитектуре.

---

## 🏗 Архитектура приложения

Система построена по принципу разделения ответственности. Nginx выступает в роли обратного прокси, обеспечивая безопасность и высокую скорость отдачи статического контента.

```mermaid
graph TD
    User((Пользователь)) -->|HTTPS / 443| Nginx{Nginx Proxy}
    
    subgraph "Frontend (Client Side)"
        Nginx -->|Static| HTML[index.html / CSS]
        HTML -->|Modules| JS[Modular JS App]
        JS -->|Client Stats| YM[Yandex Metrika / GA4]
    end

    subgraph "Backend (Server Side)"
        Nginx -->|API Proxy| FastAPI[FastAPI Server]
        FastAPI -->|ORM| DB[(PostgreSQL)]
        Nginx -->|Images| Storage[Local Image Archive]
    end

    subgraph "BI & Reporting"
        DB -->|Connector| DataLens[Yandex DataLens BI]
        DB -->|Cron Job| Script[Report Generator]
        Script -->|Excel| TG[Telegram Admin Bot]
    end
---

### 🌟 О проекте

**Gachapets** — это высокотехнологичное Fullstack-приложение, имитирующее механику призыва персонажей из популярных Gacha-игр. Проект объединяет в себе современный UI/UX, модульную архитектуру и глубокую систему бизнес-аналитики (BI).

### ✨ Ключевые фичи
- **🎯 Smart Pity System:** Алгоритм «защиты от невезения» — гарантированное выпадение легендарного персонажа на 20-й призыв.
- **📦 Модульная архитектура:** Чистый код на стороне клиента (ES6 Modules) и сервера (FastAPI), разделенный по принципам SOLID.
- **⚡ Оптимизированная доставка контента:** Раздача медиа-файлов через Nginx напрямую, что обеспечивает мгновенную загрузку даже тяжелых GIF.
- **📊 BI-интеграция:** Сквозная аналитика от клика пользователя до графиков в **Yandex DataLens**.
- **🛡 Безопасность:** Полная поддержка HTTPS (SSL от Let's Encrypt) и изоляция секретов через `.env`.

---

## 📐 Архитектура системы

```mermaid
graph TD
    User((Пользователь)) -->|HTTPS| Nginx{Nginx Reverse Proxy}
    
    subgraph "Frontend (Client)"
        Nginx -->|Static Content| HTML[index.html / CSS]
        HTML -->|ES6 Modules| JS_App[app.js / logic]
        JS_App -->|Analytics| YM[Yandex Metrika / GA4]
    end

    subgraph "Backend (VDS Server)"
        Nginx -->|API Proxy| FastAPI[FastAPI Server]
        FastAPI -->|Log Event| DB[(PostgreSQL)]
        Nginx -->|Static Images| Disk[Local Image Archive]
    end

    subgraph "Business Intelligence"
        DB -->|Data Source| DataLens[Yandex DataLens]
        DataLens -->|Visualization| Dashboard[Live Dashboard]
    end
---

### Модель Базы Данных (Star Schema)
erDiagram
    USERS ||--o{ SUMMONS : "performs"
    USERS ||--o{ UI_EVENTS : "triggers"

    USERS {
        string user_uuid PK "ID из LocalStorage"
        datetime first_seen "Дата регистрации"
        string referrer "Источник трафика"
        boolean is_mobile "Флаг устройства"
        string user_agent "Данные браузера"
    }

    SUMMONS {
        int id PK
        string user_uuid FK "Связь с профилем"
        string session_id "ID текущего визита"
        string cat_title "Имя персонажа"
        string rarity "Редкость"
        datetime timestamp "Время призыва"
    }

    UI_EVENTS {
        int id PK
        string user_uuid FK "Связь с профилем"
        string session_id "ID текущего визита"
        string event_name "Действие (open_info, etc)"
        datetime timestamp "Время события"
    }
---
