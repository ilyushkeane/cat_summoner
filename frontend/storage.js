export function getUserId() {
    let uuid = localStorage.getItem('gachapets_uuid');
    if (!uuid) {
        uuid = 'p_' + Math.random().toString(36).substr(2, 9) + Date.now();
        localStorage.setItem('gachapets_uuid', uuid);
    }
    return uuid;
}

export function getSessionId() {
    let sid = sessionStorage.getItem('gachapets_session');
    if (!sid) {
        sid = 's_' + Math.random().toString(36).substr(2, 9) + Date.now();
        sessionStorage.setItem('gachapets_session', sid);
    }
    return sid;
}

export const gameState = {
    user_uuid: getUserId(),
    session_id: getSessionId(),
    summons: parseInt(localStorage.getItem('totalCatsSummoned')) || 0,
    legendaries: parseInt(localStorage.getItem('totalLegendaries')) || 0,
    pity: parseInt(localStorage.getItem('pityCounter')) || 0,
    save() {
        localStorage.setItem('totalCatsSummoned', this.summons);
        localStorage.setItem('totalLegendaries', this.legendaries);
        localStorage.setItem('pityCounter', this.pity);
    }
};