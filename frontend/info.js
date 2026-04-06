import { personalities } from './personalities.js';

const modal = document.getElementById('info-modal');
const openBtn = document.getElementById('info-open-btn');
const closeBtn = document.getElementById('info-close-btn');
const overlay = document.querySelector('.modal-overlay');
const listContainer = document.getElementById('personalities-list');

export function initInfoModal() {
    if (!modal || !openBtn) return;

    // Генерируем список персонажей один раз при загрузке
    renderPersonalities();

    openBtn.onclick = () => {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    closeBtn.onclick = closeModal;
    overlay.onclick = closeModal;
    
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
}

function renderPersonalities() {
    if (!listContainer) return;

    const sorted = [...personalities].sort((a, b) => {
        const order = { legendary: 0, epic: 1, rare: 2, common: 3 };
        return order[a.class] - order[b.class];
    });

    listContainer.innerHTML = sorted.map(p => `
        <div class="modern-persona-item">
            <span class="p-name">${p.title}</span>
            <span class="p-tag tag-${p.class}">${p.rarity}</span>
        </div>
    `).join('');
}

function closeModal() {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}