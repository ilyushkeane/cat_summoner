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

// Логика работы (счётчик, LocalStorage, "Салют" анимация, Загрузка с фоллбеком)

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

// 4. Логика шансов выпадения (Гача-механика)
function getRandomPersona() {
    const roll = Math.random() * 100;
    let pool = [];

    if (roll < 10) { // 10% шанс
        pool = personalities.filter(p => p.class === "legendary");
    } else if (roll < 40) { // 30% шанс
        pool = personalities.filter(p => p.class === "rare");
    } else { // 60% шанс
        pool = personalities.filter(p => p.class === "common");
    }

    if (pool.length === 0) pool = personalities;
    return pool[Math.floor(Math.random() * pool.length)];
}

// 5. Главная функция призыва
function summonCat() {
    // Блокируем интерфейс
    btn.disabled = true;
    btn.textContent = "Призываем...";
    
    card.classList.add('shake-anim');
    card.classList.remove('legendary-glow');
    catImage.classList.add('hidden');
    loader.style.display = 'block';

    const persona = getRandomPersona();
    
    // Формируем URL с тегом для аутентичности
    const newImageSrc = `https://cataas.com/cat/${persona.tag}?width=400&height=400&t=${Date.now()}`;
    const downloadingImage = new Image();

    // Обработка успешной загрузки
    downloadingImage.onload = function() {
        displayCatResult(this.src, persona);
    };

    // Обработка ошибки (фоллбек на случайного кота)
    downloadingImage.onerror = function() {
        console.warn(`Фото с тегом ${persona.tag} не найдено, грузим случайное.`);
        const fallbackSrc = `https://cataas.com/cat?width=400&height=400&t=${Date.now()}`;
        const fallbackImage = new Image();
        fallbackImage.onload = function() {
            displayCatResult(this.src, persona);
        };
        fallbackImage.src = fallbackSrc;
    };

    downloadingImage.src = newImageSrc;
}

// 6. Функция отображения результата
function displayCatResult(imageSrc, persona) {
    // Небольшая задержка для завершения анимации тряски
    setTimeout(() => {
        card.classList.remove('shake-anim');
        
        // Обновляем контент
        catImage.src = imageSrc;
        catImage.classList.remove('hidden');
        loader.style.display = 'none';
        
        catTitle.textContent = persona.title;
        catDesc.textContent = persona.desc;
        catRarity.textContent = `Редкость: ${persona.rarity}`;
        
        // Обновляем стили редкости
        catRarity.className = 'rarity'; 
        catRarity.classList.add(`rare-${persona.class}`);

        // Спецэффекты для легендарок
        if (persona.class === 'legendary') {
            card.classList.add('legendary-glow');
            if (typeof confetti === 'function') {
                confetti({
                    particleCount: 150,
                    spread: 70,
                    origin: { y: 0.6 },
                    colors: ['#ff9800', '#ff5722', '#f44336']
                });
            }
        }

        // Обновляем и сохраняем статистику
        totalSummons++;
        if (totalCountDisplay) totalCountDisplay.textContent = totalSummons;
        localStorage.setItem('totalCatsSummoned', totalSummons);

        // Возвращаем кнопку в рабочее состояние
        btn.disabled = false;
        btn.innerHTML = "<span>🐾 Призвать ещё раз 🐾</span>";
    }, 600);
}

// 7. Слушатель событий
btn.addEventListener('click', summonCat);