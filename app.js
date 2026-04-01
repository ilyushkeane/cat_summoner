import { gameState, getUserId } from './frontend/storage.js';
import { trackEvent } from './frontend/analytics.js';
import * as gacha from './frontend/gacha.js';
import * as api from './frontend/api.js';
import * as ui from './frontend/ui.js';

async function handleSummon(event) {
    if (event) event.preventDefault();
    ui.setLoading(true);
    trackEvent('summon_attempt');

    try {
        // 1. Расчет результата (мозг)
        const persona = gacha.getRoll(gameState);
        gameState.save();

        // 2. Получение данных с сервера (сеть)
        const imgUrl = await api.fetchCatImage(persona.tag);

        // 3. Отображение (интерфейс)
        ui.renderResult(imgUrl, persona, gameState);

        // 4. Аналитика в БД (статистика)
        api.sendStats(persona);

    } catch (err) {
        ui.showError();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('summon-btn');
    if (btn) btn.onclick = handleSummon;

    trackEvent('app_init', { user_id: getUserId() });
});