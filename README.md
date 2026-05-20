# 🐾 Gachapets: Fullstack Analytics & Gacha System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Production-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Data--Driven-336791?logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/JavaScript-Modular%20ES6-F7DF1E?logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/Infrastructure-Nginx%20%7C%20SSL-009639?logo=nginx&logoColor=white" alt="Nginx">
</p>

**Gachapets** — это высоконагруженное по архитектуре Fullstack-приложение, сочетающее игровую механику "Гача" и комплексную систему сбора и анализа данных. Проект демонстрирует переход от простых скриптов к масштабируемой модульной архитектуре.

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
## 📊 Модель Базы Данных (Star Schema)
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
## 🚀 Ключевые Технические Фичи
### 🎮 Геймдизайн
Smart Pity System: Алгоритм гарантированного выпадения легендарного персонажа на 20-й призыв внутри сессии.
Visual Feedback: Динамическая система салютов (Confetti) и свечения карточек, зависящая от редкости.
Image Preloading: Асинхронная предзагрузка изображений перед показом, исключающая "мерцание" интерфейса.
### 📈 Аналитика и BI
Multi-Level Tracking: Комбинация внешней аналитики (YM/GA4) и собственного логирования в SQL.
Session Intelligence: Использование session_id для анализа глубины просмотра и времени сессии.
Automated Reporting: Система еженедельной выгрузки данных в Excel с доставкой через Telegram-бота.
Live BI: Интеграция с Yandex DataLens для мониторинга Drop-rate и DAU в реальном времени.

---
## 📁 Структура Проекта
├── backend/            # Логика подключения к БД и SQLAlchemy модели
├── frontend/           # Модульная логика клиента (API, UI, Storage)
├── static/cats/        # Модерируемый архив изображений по тегам
├── style/              # Стили и анимации
├── main.py             # Точка входа FastAPI сервера
├── app.js              # Главный оркестратор фронтенда
└── index.html          # Стартовая страница

--
