import { trackEvent } from './analytics.js';

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
    if (!elements.btn) return;
    elements.btn.disabled = isLoading;
    
    if (isLoading) {
        elements.btn.textContent = "Призываем...";
        elements.card?.classList.add('shake-anim');
        elements.catImage?.classList.add('hidden');
        if (elements.loader) elements.loader.style.display = 'block';
    } else {
        elements.btn.innerHTML = "<span>🐾 Призвать ещё раз 🐾</span>";
        elements.card?.classList.remove('shake-anim');
        if (elements.loader) elements.loader.style.display = 'none';
        elements.catImage?.classList.remove('hidden');
    }
}

export function renderResult(imgUrl, persona, state) {
    try {
        if (elements.catImage) elements.catImage.src = imgUrl;
        if (elements.catTitle) elements.catTitle.textContent = persona.title;
        if (elements.catDesc) elements.catDesc.textContent = persona.desc;
        if (elements.catRarity) {
            elements.catRarity.textContent = `Редкость: ${persona.rarity}`;
            elements.catRarity.className = `rarity rare-${persona.class}`;
        }

        elements.card?.classList.remove('legendary-glow', 'epic-glow');

        state.summons++;
        if (elements.totalCount) elements.totalCount.textContent = state.summons;

        if (persona.class === 'epic') {
            elements.card?.classList.add('epic-glow');
            triggerConfetti('epic');
        }

        if (persona.class === 'legendary') {
            state.legendaries++;
            if (elements.legCount) elements.legCount.textContent = state.legendaries;
            elements.card?.classList.add('legendary-glow');
            triggerConfetti('legendary');
        }
    } catch (err) {
        console.error("Ошибка при отрисовке:", err);
    } finally {
        // Кнопка ДОЛЖНА включиться в любом случае
        setLoading(false);
    }
}

export function showError() {
    setLoading(false);
    if (elements.btn) elements.btn.innerHTML = "<span>🐾 Ошибка сервера 🐾</span>";
}

function triggerConfetti(type) {
    if (typeof confetti !== 'function') return;
    if (type === 'epic') {
        confetti({ particleCount: 60, spread: 50, origin: { y: 0.7 }, colors: ['#9c27b0', '#e1bee7', '#ffffff'] });
    } else {
        confetti({ particleCount: 250, spread: 100, origin: { y: 0.6 }, colors: ['#ff9800', '#ffffff', '#ffd700'] });
    }
}