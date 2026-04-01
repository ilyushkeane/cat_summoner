import { gameState, getUserId } from './frontend/storage.js';
import { trackEvent } from './frontend/analytics.js';
import * as gacha from './frontend/gacha.js';
import * as api from './frontend/api.js';
import * as ui from './frontend/ui.js';

async function handleSummon(event) {
    if (event) event.preventDefault();
    
    // Если уже призываем — игнорируем клик
    const btn = document.getElementById('summon-btn');
    if (btn.disabled) return;

    ui.setLoading(true);
    trackEvent('summon_attempt');

    const startTime = Date.now();
    const minimumWait = 1200; // 1.2 секунды анимации

    try {
        // 1. Делаем ролл
        const persona = gacha.getRoll(gameState);

        // 2. Начинаем загрузку картинки (параллельно анимации)
        const imgUrl = await api.fetchCatImage(persona.tag);

        // 3. Вычисляем, сколько еще нужно подождать до конца тряски
        const elapsedTime = Date.now() - startTime;
        const remainingWait = Math.max(0, minimumWait - elapsedTime);

        // Ждем остаток времени и только ТОГДА обновляем экран
        setTimeout(() => {
            ui.renderResult(imgUrl, persona, gameState);
            gameState.save(); // Сохраняем стейт только при успехе
            api.sendStats(persona);
        }, remainingWait);

    } catch (err) {
        ui.showError();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('summon-btn');
    if (btn) btn.onclick = handleSummon;
    
    // Первый запуск
    handleSummon();

    trackEvent('app_init', { user_id: getUserId() });
});