import { METRICA_ID } from './config.js';

/**
 * Универсальная функция для трекинга событий
 * @param {string} eventName - Название события (цели)
 * @param {object} params - Дополнительные параметры события
 */
export function trackEvent(eventName, params = {}) {
    // 1. Отправка в Google Analytics (GA4)
    // Проверяем наличие функции gtag, которую подключаем в index.html
    if (typeof gtag === 'function') {
        gtag('event', eventName, params);
    }
    
    // 2. Отправка в Яндекс.Метрику
    // Используем метод reachGoal для достижения целей
    if (typeof ym === 'function') {
        ym(METRICA_ID, 'reachGoal', eventName, params);
    }
    
    // 3. Логирование в консоль (полезно для разработки)
    // Показывает, какие данные улетают в аналитику прямо сейчас
    console.log(`📊 [Analytics] Событие: ${eventName}`, params);
}

/**
 * Специальная функция для передачи параметров пользователя (User Params)
 * Помогает связать UUID из базы с сессией в Метрике
 * @param {string} userId - UUID пользователя
 */
export function setUserParams(userId) {
    if (typeof ym === 'function') {
        ym(METRICA_ID, 'userParams', { userID: userId });
    }
    
    if (typeof gtag === 'function') {
        gtag('set', 'user_properties', { user_id: userId });
    }
}