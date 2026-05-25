import { API_URL } from './config.js';
import { getUserId, getSessionId } from './storage.js';

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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_uuid: getUserId(),
                session_id: getSessionId(),
                cat_title: persona.title,
                rarity: persona.class,
                referrer: document.referrer || "direct",
                user_agent: navigator.userAgent,
                is_mobile: /iPhone|Android/i.test(navigator.userAgent)
            })
        });
    } catch (e) { console.warn("DB Log failed"); }
}

export async function sendEvent(eventName) {
    try {
        await fetch(`${API_URL}/event`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_uuid: getUserId(),
                session_id: getSessionId(),
                event_name: eventName
            })
        });
    } catch (e) { }
}