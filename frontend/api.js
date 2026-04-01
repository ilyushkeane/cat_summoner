import { API_URL } from './config.js';
import { getUserId } from './storage.js';

export async function fetchCatImage(tag) {
    const url = `${API_URL}/get_cat/${tag}?t=${Date.now()}`;
    
    // Создаем промис, который зарезолвится только когда картинка СКАЧАЕТСЯ целиком
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(url); // Картинка готова
        img.onerror = () => reject(new Error("Image load error"));
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
    } catch (e) { console.warn("Статистика не сохранена"); }
}