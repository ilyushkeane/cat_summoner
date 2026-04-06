Привет!    
# 🐾 Gachapets: Fullstack Gacha Experience

<p align="center">
  <img src="img/preview.png" alt="Gachapets Preview" width="600">
</p>

<p align="center">
  <a href="https://gachapets.ru"><strong>🚀 Посмотреть Live Demo</strong></a> | 
  <a href="https://datalens.yandex/49wwzmqrnts0o"><strong>📊 Открытая аналитика</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
  <img src="https://img.shields.io/badge/Frontend-ES6%20Modules-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS">
</p>

---

## 🌟 О проекте

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

## 🛠 Технологический стек
Слой	Технологии
Frontend	JavaScript (ES6+), CSS3 (Glassmorphism), HTML5, Canvas-Confetti
Backend	Python 3.12, FastAPI, SQLAlchemy, Pydantic, Gunicorn
DevOps	Ubuntu Linux, Nginx, Systemd, Certbot (SSL)
Database	PostgreSQL
Analytics	Yandex Metrika, Google Analytics 4, Yandex DataLens
