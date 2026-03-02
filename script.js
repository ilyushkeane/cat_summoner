//1.
  const personalities = [
    // ОБЫЧНЫЕ (Common) - 11 персонажей
    { 
        title: "Картонный Барон", tag: "box", rarity: "Обычный", class: "common",
        desc: "Твоя крепость — коробка от обуви. Пусть сегодня все твои границы будут под надежной защитой!" 
    },
    { 
        title: "Профессиональный Соня", tag: "sleepy", rarity: "Обычный", class: "common",
        desc: "Ты мастер бесконтактного сна в любой позе. Желаю, чтобы подушка сегодня была идеально мягкой!" 
    },
    { 
        title: "Белое Облачко", tag: "white", rarity: "Обычный", class: "common",
        desc: "Ты чист и пушист, как свежий зефир. Пусть этот день пройдет легко и воздушно!" 
    },
    { 
        title: "Теневой Ниндзя", tag: "black", rarity: "Обычный", class: "common",
        desc: "Тебя не видно в темноте, ты сама грация. Желаю мастерски обходить все острые углы и неприятности!" 
    },
    { 
        // ИСПРАВЛЕНО: Теперь любой взгляд кота объясняется философией
        title: "Загадочный Философ", tag: "window", rarity: "Обычный", class: "common",
        desc: "Ты познал дзен, созерцая невидимое. Пусть твой глубокий взор сегодня поможет увидеть новые возможности во всём!" 
    },
    { 
        title: "Мимимишный Тиран", tag: "cute", rarity: "Обычный", class: "common",
        desc: "Один твой взгляд заставляет людей отдавать всё. Пусть перед твоим обаянием сегодня откроются все двери!" 
    },
    { 
        title: "Вечный Котёнок", tag: "kitten", rarity: "Обычный", class: "common",
        desc: "В душе тебе всегда три месяца. Желаю сохранять детское любопытство и радоваться каждой мелочи!" 
    },
    { 
        title: "Инструктор по Йоге", tag: "stretch", rarity: "Обычный", class: "common",
        desc: "Твоей растяжке позавидуют олимпийцы. Пусть твой день будет гибким и подстраивается под тебя!" 
    },
    { 
        title: "Снежный Комочек", tag: "snow", rarity: "Обычный", class: "common",
        desc: "Ты воплощение зимнего уюта. Желаю, чтобы даже в самую холодную погоду тебя согревали добрые слова!" 
    },
    { 
        title: "Игривый Вихрь", tag: "play", rarity: "Обычный", class: "common",
        desc: "Ты не можешь пройти мимо шуршащей бумажки. Желаю тебе найти источник бесконечной энергии и радости!" 
    },
    { 
        title: "Рыжая Улыбка", tag: "orange", rarity: "Обычный", class: "common",
        desc: "Рыжие коты — это концентрированное солнце. Пусть твое настроение сегодня сияет ярче всех!" 
    },

    // РЕДКИЕ (Rare) - 10 персонажей
    { 
        title: "Офисный Планктон", tag: "computer", rarity: "Редкий", class: "rare",
        desc: "Ты лучше всех знаешь, как согреть ноутбук. Пусть работа сегодня «не виснет», а дедлайны мурлыкают!" 
    },
    { 
        title: "Генеральный Директор", tag: "tie", rarity: "Редкий", class: "rare",
        desc: "Галстук надет, взгляд суров. Желаю сегодня успешно провести все переговоры и получить премию!" 
    },
    { 
        title: "Олимпийский Прыгун", tag: "jump", rarity: "Редкий", class: "rare",
        desc: "Гравитация? Нет, не слышал. Желаю тебе сегодня совершить головокружительный скачок к своей мечте!" 
    },
    { 
        title: "Пищевой Критик", tag: "eat", rarity: "Редкий", class: "rare",
        desc: "Ты не ешь, ты дегустируешь. Пусть сегодня всё, что ты пробуешь, приносит гастрономический восторг!" 
    },
    { 
        title: "Грозный Кусь", tag: "bite", rarity: "Редкий", class: "rare",
        desc: "Маленький, но очень решительный. Желаю тебе сегодня железной хватки в достижении своих целей!" 
    },
    { 
        title: "Оперная Дива", tag: "sing", rarity: "Редкий", class: "rare",
        desc: "Твой мяу слышен в соседнем районе. Желаю, чтобы сегодня тебя слушали с замиранием сердца!" 
    },
    { 
        title: "Пушистый Хаос", tag: "funny", rarity: "Редкий", class: "rare",
        desc: "Где ты — там праздник и легкий беспорядок. Пусть этот день принесет много смеха и приключений!" 
    },
    { 
        title: "Кото-Модель", tag: "prowl", rarity: "Редкий", class: "rare",
        desc: "Ты рожден для подиума. Желаю, чтобы каждый твой шаг сегодня был уверенным и стильным!" 
    },
    { 
        title: "Профессор Мяу", tag: "glasses", rarity: "Редкий", class: "rare",
        desc: "Твой интеллект виден издалека. Желаю тебе сегодня найти ответы на все самые сложные вопросы бытия!" 
    },
    { 
        title: "Грустный Романтик", tag: "sad", rarity: "Редкий", class: "rare",
        desc: "Твои глаза полны светлой грусти. Пусть сегодня найдется повод для искренней радости!" 
    },

    // ЭПИЧЕСКИЕ (Epic) - 3 новых персонажа
    { 
        title: "Кото-Пират", tag: "costume", rarity: "Эпический", class: "epic",
        desc: "Йо-хо-хо! Сокровище (твоя миска) уже близко. Желаю попутного ветра и верного курса во всех сегодняшних начинаниях!" 
    },
    { 
        title: "Супер-Кот", tag: "costume", rarity: "Эпический", class: "epic",
        desc: "Твой плащ шуршит громче всех в этом районе. Пусть сегодня твои суперспособности помогут спасти мир или хотя бы выспаться!" 
    },
    { 
        title: "Пчело-Кот", tag: "costume", rarity: "Эпический", class: "epic",
        desc: "Ты слишком сладкий, чтобы жалить. Желаю максимально продуктивного дня и побольше «цветочного» нектара в виде вкусного кофе!" 
    },

    // ЛЕГЕНДАРНЫЕ (Legendary) - 2 персонажа
    { 
        title: "Властелин Прайда", tag: "lion", rarity: "Легендарный", class: "legendary",
        desc: "Королевская кровь течет в твоих жилах. Ты — истинный монарх этого дивана. Пусть мир склонится перед твоим величием!" 
    },
    { 
        title: "Гроза Джунглей", tag: "tiger", rarity: "Легендарный", class: "legendary",
        desc: "Твои полоски — знак высшей доблести. Ты хищник, которого боятся даже тапочки. Желаю тебе сегодня великой охоты!" 
    }
];

const API_URL = "http://127.0.0.1:8000/api";

// Твои настройки аналитики
const METRICA_ID = 107060992; // Твой ID Яндекса

/**
 * Универсальная функция для отправки событий во все системы сразу
 * @param {string} eventName - Название события (например, 'summon_click')
 * @param {object} params - Дополнительные данные (например, { rarity: 'legendary' })
 */
function trackEvent(eventName, params = {}) {
    // 1. Отправка в Google Analytics
    if (typeof gtag === 'function') {
        gtag('event', eventName, params);
    }
    
    // 2. Отправка в Яндекс.Метрику
    if (typeof ym === 'function') {
        ym(METRICA_ID, 'reachGoal', eventName, params);
    }

    console.log(`📊 [Analytics] Событие: ${eventName}`, params);
}


// 1. Функция для создания или получения ID пользователя из памяти браузера
function getUserId() {
    let uuid = localStorage.getItem('gachapets_uuid');
    if (!uuid) {
        // Создаем случайный ID, если его нет
        uuid = 'p_' + Math.random().toString(36).substr(2, 9) + Date.now();
        localStorage.setItem('gachapets_uuid', uuid);
    }
    return uuid;
}

// 2. Функция отправки данных на твой сервер (Бэкенд)
async function sendDataToServer(persona) {
    const payload = {
        user_uuid: getUserId(),
        cat_title: persona.title,
        rarity: persona.class
    };

    console.log("🚀 Отправляю данные в базу:", payload);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const result = await response.json();
            console.log("✅ Ответ сервера:", result);
        }
    } catch (e) {

        trackEvent('technical_error', { 
        error_type: 'fetch_error',
        message: e.message 
    });

        // Если бэкенд выключен, мы просто пишем в консоль, чтобы кнопка не зависала
        console.warn("⚠️ Не удалось сохранить в БД (возможно, бэкенд выключен):", e);
    }
}

// 2. Элементы DOM
const btn = document.getElementById('summon-btn');
const card = document.getElementById('card');
const catImage = document.getElementById('cat-image');
const catTitle = document.getElementById('cat-title');
const catDesc = document.getElementById('cat-desc');
const catRarity = document.getElementById('cat-rarity');
const loader = document.getElementById('loader');
const totalCountDisplay = document.getElementById('total-count');

// 3. Инициализация статистики из памяти браузера
let totalSummons = parseInt(localStorage.getItem('totalCatsSummoned')) || 0;
if (totalCountDisplay) totalCountDisplay.textContent = totalSummons;

// 3. Логика Гачи
function getRandomPersona() {
    const roll = Math.random() * 100;
    let pool = [];

    if (roll < 5) pool = personalities.filter(p => p.class === "legendary");
    else if (roll < 20) pool = personalities.filter(p => p.class === "epic");
    else if (roll < 45) pool = personalities.filter(p => p.class === "rare");
    else pool = personalities.filter(p => p.class === "common");

    return pool[Math.floor(Math.random() * pool.length)];
}

// 4. Функция призыва
function summonCat(event) {
    if (event) event.preventDefault();
    if (btn.disabled) return;

    trackEvent('summon_attempt'); // Пользователь нажал кнопку

    btn.disabled = true;
    btn.textContent = "Призываем...";
    card.classList.add('shake-anim');
    card.classList.remove('legendary-glow', 'epic-glow');
    catImage.classList.add('hidden');
    loader.style.display = 'block';

    const persona = getRandomPersona();
    
    // Запрашиваем картинку у нашего бэкенда
    const newImageSrc = `http://127.0.0.1:8000/api/get_cat/${persona.tag}?t=${Date.now()}`;
    
    const downloadingImage = new Image();
    downloadingImage.onload = function() {
        displayCatResult(this.src, persona);
    };
    downloadingImage.onerror = function() {
        // Фоллбек если наш сервак не отдал картинку
        console.error("Ошибка загрузки локального фото");
        btn.disabled = false;
        btn.innerHTML = "<span>🐾 Ошибка сервера 🐾</span>";
    };
    downloadingImage.src = newImageSrc;
}

// 6. Функция отображения результата
function displayCatResult(imageSrc, persona) {
    setTimeout(() => {
        card.classList.remove('shake-anim');
        catImage.src = imageSrc;
        catImage.classList.remove('hidden');
        loader.style.display = 'none';
        
        catTitle.textContent = persona.title;
        catDesc.textContent = persona.desc;
        catRarity.textContent = `Редкость: ${persona.rarity}`;
        catRarity.className = `rarity rare-${persona.class}`;

        if (persona.class === 'epic') card.classList.add('epic-glow');
        if (persona.class === 'legendary') card.classList.add('legendary-glow');

        // Отправляем в БД!
        sendDataToServer(persona);

        btn.disabled = false;
        btn.innerHTML = "<span>🐾 Призвать ещё раз 🐾</span>";
    }, 600);

    // Трекаем, что конкретно выпало
    trackEvent('cat_summon_success', {
        cat_name: persona.title,
        rarity: persona.class,
        user_id: getUserId()
    });

    // Отдельное событие для Легендарок (для настройки рекламы или целей)
    if (persona.class === 'legendary') {
        trackEvent('legendary_drop', { cat_name: persona.title });
    }
}

// 7. Слушатель событий
btn.onclick = (event) => {
    summonCat(event);
    return false;
};

window.addEventListener('DOMContentLoaded', () => {
    const uuid = getUserId();
    trackEvent('app_init', { 
        user_id: uuid,
        screen_size: window.innerWidth + 'x' + window.innerHeight
    });
});