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
        elements.card.classList.remove('legendary-glow', 'epic-glow');
        elements.catImage.classList.add('hidden');
        elements.loader.style.display = 'block';
    } else {
        elements.card.classList.remove('shake-anim');
        elements.loader.style.display = 'none';
        elements.catImage.classList.remove('hidden');
    }
}

export function renderResult(imgUrl, persona, state) {
    setLoading(false);
    elements.catImage.src = imgUrl;
    elements.catTitle.textContent = persona.title;
    elements.catDesc.textContent = persona.desc;
    elements.catRarity.textContent = `Редкость: ${persona.rarity}`;
    elements.catRarity.className = `rarity rare-${persona.class}`;

    state.summons++;
    elements.totalCount.textContent = state.summons;

    if (persona.class === 'epic') elements.card.classList.add('epic-glow');
    
    if (persona.class === 'legendary') {
        state.legendaries++;
        elements.legCount.textContent = state.legendaries;
        elements.card.classList.add('legendary-glow');
        launchConfetti();
    }
    elements.btn.innerHTML = "<span>🐾 Призвать ещё раз 🐾</span>";
}

function launchConfetti() {
    if (typeof confetti === 'function') {
        confetti({ particleCount: 250, spread: 100, origin: { y: 0.6 }, colors: ['#ff9800', '#ffffff', '#ffd700'] });
    }
}

export function showError() {
    setLoading(false);
    elements.btn.innerHTML = "<span>🐾 Ошибка сервера 🐾</span>";
}