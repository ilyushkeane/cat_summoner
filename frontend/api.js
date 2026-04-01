import { API_URL } from './config.js'; // Точка означает "в этой же папке"
import { getUserId } from './storage.js';

export async function fetchCatImage(tag) {
    const response = await fetch(`${API_URL}/get_cat/${tag}?t=${Date.now()}`);
    if (!response.ok) throw new Error("API Error");
    return response.url;
}

export async function sendStats(persona) {
    try {
        await fetch(`${API_URL}/log`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_uuid: getUserId(),
                cat_title: persona.title,
                rarity: persona.class
            })
        });
    } catch (e) { console.warn("Статистика не сохранена"); }
}