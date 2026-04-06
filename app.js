import { gameState, getUserId } from './frontend/storage.js';
import { trackEvent } from './frontend/analytics.js';
import { initInfoModal } from './frontend/info.js';
import * as gacha from './frontend/gacha.js';
import * as api from './frontend/api.js';
import * as ui from './frontend/ui.js';

async function handleSummon(event) {
    if (event) event.preventDefault();
    
    const btn = document.getElementById('summon-btn');
    if (btn && btn.disabled) return;

    ui.setLoading(true);
    const startTime = Date.now();

    try {
        const persona = gacha.getRoll(gameState);
        const imgUrl = await api.fetchCatImage(persona.tag);

        const elapsedTime = Date.now() - startTime;
        const wait = Math.max(0, 800 - elapsedTime);

        setTimeout(() => {
            ui.renderResult(imgUrl, persona, gameState);
            gameState.save();
            api.sendStats(persona);
            trackEvent('cat_summon_success', { name: persona.title, rarity: persona.class });
        }, wait);

    } catch (err) {
        console.error("Ошибка:", err);
        ui.showError();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('summon-btn');
    if (btn) btn.onclick = handleSummon;
    
    initInfoModal();

    // --- ПРОВЕРКА СОСТОЯНИЯ ПРИ ВХОДЕ ---
    ui.updateCounterDisplay(gameState); 

    trackEvent('app_init', { user_id: getUserId() });
});