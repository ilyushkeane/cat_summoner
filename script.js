// --- 1. БАЗА ДАННЫХ ПЕРСОНАЖЕЙ ---
const personalities = [
    // ОБЫЧНЫЕ (Common)
    { title: "Картонный Барон", tag: "box", rarity: "Обычный", class: "common", desc: "Твоя крепость — коробка от обуви. Пусть сегодня все твои границы будут под надежной защитой!" },
    { title: "Профессиональный Соня", tag: "sleepy", rarity: "Обычный", class: "common", desc: "Ты мастер бесконтактного сна в любой позе. Желаю, чтобы подушка сегодня была идеально мягкой!" },
    { title: "Белое Облачко", tag: "white", rarity: "Обычный", class: "common", desc: "Ты чист и пушист, как свежий зефир. Пусть этот день пройдет легко и воздушно!" },
    { title: "Теневой Ниндзя", tag: "black", rarity: "Обычный", class: "common", desc: "Тебя не видно в темноте, ты сама грация. Желаю мастерски обходить все острые углы и неприятности!" },
    { title: "Загадочный Философ", tag: "window", rarity: "Обычный", class: "common", desc: "Ты познал дзен, созерцая невидимое. Пусть твой глубокий взор сегодня поможет увидеть новые возможности во всём!" },
    { title: "Мимимишный Тиран", tag: "cute", rarity: "Обычный", class: "common", desc: "Один твой взгляд заставляет людей отдавать всё. Пусть перед твоим обаянием сегодня откроются все двери!" },
    { title: "Вечный Котёнок", tag: "kitten", rarity: "Обычный", class: "common", desc: "В душе тебе всегда три месяца. Желаю сохранять детское любопытство и радоваться каждой мелочи!" },
    { title: "Инструктор по Йоге", tag: "stretch", rarity: "Обычный", class: "common", desc: "Твоей растяжке позавидуют олимпийцы. Пусть твой день будет гибким и подстраивается под тебя!" },
    { title: "Снежный Комочек", tag: "snow", rarity: "Обычный", class: "common", desc: "Ты воплощение зимнего уюта. Желаю, чтобы даже в самую холодную погоду тебя согревали добрые слова!" },
    { title: "Игривый Вихрь", tag: "play", rarity: "Обычный", class: "common", desc: "Ты не можешь пройти мимо шуршащей бумажки. Желаю тебе найти источник бесконечной энергии и радости!" },
    { title: "Рыжая Улыбка", tag: "orange", rarity: "Обычный", class: "common", desc: "Рыжие коты — это концентрированное солнце. Пусть твое настроение сегодня сияет ярче всех!" },

    // РЕДКИЕ (Rare)
    { title: "Офисный Планктон", tag: "computer", rarity: "Редкий", class: "rare", desc: "Ты лучше всех знаешь, как согреть ноутбук. Пусть работа сегодня «не виснет», а дедлайны мурлыкают!" },
    { title: "Генеральный Директор", tag: "tie", rarity: "Редкий", class: "rare", desc: "Галстук надет, взгляд суров. Желаю сегодня успешно провести все переговоры и получить премию!" },
    { title: "Олимпийский Прыгун", tag: "jump", rarity: "Редкий", class: "rare", desc: "Гравитация? Нет, не слышал. Желаю тебе сегодня совершить головокружительный скачок к своей мечте!" },
    { title: "Пищевой Критик", tag: "eat", rarity: "Редкий", class: "rare", desc: "Ты не ешь, ты дегустируешь. Пусть сегодня всё, что ты пробуешь, приносит гастрономический восторг!" },
    { title: "Грозный Кусь", tag: "bite", rarity: "Редкий", class: "rare", desc: "Маленький, но очень решительный. Желаю тебе сегодня железной хватки в достижении своих целей!" },
    { title: "Оперная Дива", tag: "sing", rarity: "Редкий", class: "rare", desc: "Твой мяу слышен в соседнем районе. Желаю, чтобы сегодня тебя слушали с замиранием сердца!" },
    { title: "Пушистый Хаос", tag: "funny", rarity: "Редкий", class: "rare", desc: "Где ты — там праздник и легкий беспорядок. Пусть этот день принесет много смеха и приключений!" },
    { title: "Кото-Модель", tag: "prowl", rarity: "Редкий", class: "rare", desc: "Ты рожден для подиума. Желаю, чтобы каждый твой шаг сегодня был уверенным и стильным!" },
    { title: "Профессор Мяу", tag: "glasses", rarity: "Редкий", class: "rare", desc: "Твой интеллект виден издалека. Желаю тебе сегодня найти ответы на все самые сложные вопросы бытия!" },
    { title: "Грустный Романтик", tag: "sad", rarity: "Редкий", class: "rare", desc: "Твои глаза полны светлой грусти. Пусть сегодня найдется повод для искренней радости!" },

    // ЭПИЧЕСКИЕ (Epic)
    { title: "Кото-Пират", tag: "costumeb-pirate", rarity: "Эпический", class: "epic", desc: "Йо-хо-хо! Сокровище (твоя миска) уже близко. Желаю попутного ветра во всех начинаниях!" },
    { title: "Супер-Кот", tag: "costume-superhero", rarity: "Эпический", class: "epic", desc: "Твой плащ шуршит громче всех. Пусть твои суперспособности помогут спасти мир или хотя бы выспаться!" },
    { title: "Пчело-Кот", tag: "costume-bee", rarity: "Эпический", class: "epic", desc: "Ты слишком сладкий, чтобы жалить. Желаю максимально продуктивного дня и побольше вкусного кофе!" },

    // ЛЕГЕНДАРНЫЕ (Legendary)
    { title: "Властелин Прайда", tag: "lion", rarity: "Легендарный", class: "legendary", desc: "Королевская кровь течет в твоих жилах. Ты истинный монарх. Пусть мир склонится перед твоим величием!" },
    { title: "Гроза Джунглей", tag: "tiger", rarity: "Легендарный", class: "legendary", desc: "Твои полоски — знак высшей доблести. Ты хищник, которого боятся даже тапочки. Желаю тебе великой охоты!" }
];

// --- 2. КОНФИГУРАЦИЯ ---
// На сервере используем "/api", локально можно менять на "http://127.0.0.1:8000/api"
const API_URL = (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") 
    ? "http://127.0.0.1:8000/api" 
    : "/api";

const METRICA_ID = 107060992; 

// --- 3. ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ---
let totalSummons = parseInt(localStorage.getItem('totalCatsSummoned')) || 0;
let totalLegendaries = parseInt(localStorage.getItem('totalLegendaries')) || 0;
let pityCounter = parseInt(localStorage.getItem('pityCounter')) || 0;

const btn = document.getElementById('summon-btn');
const card = document.getElementById('card');
const catImage = document.getElementById('cat-image');
const catTitle = document.getElementById('cat-title');
const catDesc = document.getElementById('cat-desc');
const catRarity = document.getElementById('cat-rarity');
const loader = document.getElementById('loader');
const totalCountDisplay = document.getElementById('total-count');
const legCountDisplay = document.getElementById('leg-count');

if (totalCountDisplay) totalCountDisplay.textContent = totalSummons;
if (legCountDisplay) legCountDisplay.textContent = totalLegendaries;

// --- 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
function trackEvent(eventName, params = {}) {
    if (typeof gtag === 'function') gtag('event', eventName, params);
    if (typeof ym === 'function') ym(METRICA_ID, 'reachGoal', eventName, params);
    console.log(`📊 [Analytics] ${eventName}`, params);
}

function getUserId() {
    let uuid = localStorage.getItem('gachapets_uuid');
    if (!uuid) {
        uuid = 'p_' + Math.random().toString(36).substr(2, 9) + Date.now();
        localStorage.setItem('gachapets_uuid', uuid);
    }
    return uuid;
}

async function sendDataToServer(persona) {
    const payload = {
        user_uuid: getUserId(),
        cat_title: persona.title,
        rarity: persona.class
    };

    try {
        await fetch(`${API_URL}/log`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
    } catch (e) {
        trackEvent('technical_error', { error_type: 'fetch_error', message: e.message });
        console.warn("⚠️ Ошибка записи в БД:", e);
    }
}

function getRandomPersona() {
    pityCounter++;
    const roll = Math.random() * 100;
    let pool = [];

    if (pityCounter >= 20) {
        console.log("💎 ГАРАНТ на 20-й крутке!");
        pool = personalities.filter(p => p.class === "legendary");
    } else if (roll < 5) {
        pool = personalities.filter(p => p.class === "legendary");
    } else if (roll < 20) {
        pool = personalities.filter(p => p.class === "epic");
    } else if (roll < 45) {
        pool = personalities.filter(p => p.class === "rare");
    } else {
        pool = personalities.filter(p => p.class === "common");
    }

    const selected = pool[Math.floor(Math.random() * pool.length)];

    if (selected.class === 'legendary') {
        pityCounter = 0;
    }
    localStorage.setItem('pityCounter', pityCounter);
    return selected;
}

// --- 5. ОСНОВНАЯ ЛОГИКА ---
function summonCat(event) {
    if (event) event.preventDefault();
    if (btn.disabled) return;

    trackEvent('summon_attempt');

    btn.disabled = true;
    btn.textContent = "Призываем...";
    card.classList.add('shake-anim');
    card.classList.remove('legendary-glow', 'epic-glow');
    catImage.classList.add('hidden');
    loader.style.display = 'block';

    const persona = getRandomPersona();
    const newImageSrc = `${API_URL}/get_cat/${persona.tag}?t=${Date.now()}`;
    
    const downloadingImage = new Image();
    downloadingImage.onload = function() {
        displayCatResult(this.src, persona);
    };
    downloadingImage.onerror = function() {
        console.error("Ошибка загрузки фото");
        btn.disabled = false;
        btn.innerHTML = "<span>🐾 Ошибка сервера 🐾</span>";
    };
    downloadingImage.src = newImageSrc;
}

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

        if (persona.class === 'epic') {
            card.classList.add('epic-glow');
            confetti({ particleCount: 100, spread: 60, origin: { y: 0.7 } });
        }
        
        if (persona.class === 'legendary') {
            totalLegendaries++;
            if (legCountDisplay) legCountDisplay.textContent = totalLegendaries;
            localStorage.setItem('totalLegendaries', totalLegendaries);
            
            card.classList.add('legendary-glow');
            confetti({
                particleCount: 250, spread: 100, origin: { y: 0.6 },
                colors: ['#ff9800', '#ffffff', '#ffd700']
            });
            trackEvent('legendary_drop', { cat_name: persona.title });
        }

        totalSummons++;
        if (totalCountDisplay) totalCountDisplay.textContent = totalSummons;
        localStorage.setItem('totalCatsSummoned', totalSummons);

        sendDataToServer(persona);
        
        trackEvent('cat_summon_success', {
            cat_name: persona.title,
            rarity: persona.class,
            user_id: getUserId()
        });

        btn.disabled = false;
        btn.innerHTML = "<span>🐾 Призвать ещё раз 🐾</span>";
    }, 600);
}

// --- 6. СОБЫТИЯ ---
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