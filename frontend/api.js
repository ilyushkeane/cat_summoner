import { API_URL } from './config.js';
import { getUserId } from './storage.js';

export async function fetchCatImage(tag) {
    const url = `${API_URL}/get_cat/${tag}?t=${Date.now()}`;
    
    return new Promise((resolve, reject) => {
        const img = new Image();
        // Тайм-аут на случай, если сервер или сеть тормозят
        const timeout = setTimeout(() => reject(new Error("Timeout")), 10000);

        img.onload = () => {
            clearTimeout(timeout);
            resolve(url);
        };
        img.onerror = () => {
            clearTimeout(timeout);
            reject(new Error("Load Error"));
        };
        img.src = url;
    });
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
    } catch (e) {
        console.warn("📊 Статистика не сохранена, но игра продолжается");
    }
}