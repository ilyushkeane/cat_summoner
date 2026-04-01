const elements = {
    btn: document.getElementById('summon-btn'),
    card: document.getElementById('card'),
    catImage: document.getElementById('cat-image'),
    catTitle: document.getElementById('cat-title'),
    catDesc: document.getElementById('cat-desc'),
    catRarity: document.getElementById('cat-rarity'),
    loader: document.getElementById('loader'),
    totalCount: document.getElementById('total-count'),
    legCount: document.getElementById('leg-count')
};

export function setLoading(isLoading) {
    elements.btn.disabled = isLoading;
    if (isLoading) {
        elements.btn.textContent = "Призываем...";
        elements.card.classList.add('shake-anim');
        // Прячем старую картинку, чтобы не было "перескока"
        elements.catImage.classList.add('hidden');
        elements.loader.style.display = 'block';
    } else {
        elements.card.classList.remove('shake-anim');
        elements.loader.style.display = 'none';
        elements.catImage.classList.remove('hidden');
    }
}

export function renderResult(imgUrl, persona, state) {
    // Сначала обновляем все данные в памяти DOM
    elements.catImage.src = imgUrl;
    elements.catTitle.textContent = persona.title;
    elements.catDesc.textContent = persona.desc;
    elements.catRarity.textContent = `Редкость: ${persona.rarity}`;
    
    // Очищаем старые классы редкости и ставим новый
    elements.catRarity.className = `rarity rare-${persona.class}`;
    elements.card.classList.remove('legendary-glow', 'epic-glow');

    // Теперь, когда всё готово, выключаем лоадер и показываем карточку
    setLoading(false);

    // Прибавляем счетчик
    state.summons++;
    elements.totalCount.textContent = state.summons;

    // Спецэффекты
    if (persona.class === 'epic') {
        elements.card.classList.add('epic-glow');
        triggerConfetti('epic');
    }

    if (persona.class === 'legendary') {
        state.legendaries++;
        elements.legCount.textContent = state.legendaries;
        elements.card.classList.add('legendary-glow');
        triggerConfetti('legendary');
    }
}

function triggerConfetti(type) {
    if (typeof confetti !== 'function') return;
    
    if (type === 'epic') {
        confetti({
            particleCount: 60,
            spread: 50,
            origin: { y: 0.7 },
            colors: ['#9c27b0', '#e1bee7', '#ffffff']
        });
    } else {
        confetti({
            particleCount: 250,
            spread: 100,
            origin: { y: 0.6 },
            colors: ['#ff9800', '#ffffff', '#ffd700']
        });
    }
}

export function showError() {
    setLoading(false);
    elements.btn.innerHTML = "<span>🐾 Ошибка сервера 🐾</span>";
}