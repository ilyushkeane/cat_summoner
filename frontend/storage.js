export function getUserId() {
    let uuid = localStorage.getItem('gachapets_uuid');
    if (!uuid) {
        uuid = 'p_' + Math.random().toString(36).substr(2, 9) + Date.now();
        localStorage.setItem('gachapets_uuid', uuid);
    }
    return uuid;
}

export const gameState = {
    summons: parseInt(localStorage.getItem('totalCatsSummoned')) || 0,
    legendaries: parseInt(localStorage.getItem('totalLegendaries')) || 0,
    pity: parseInt(localStorage.getItem('pityCounter')) || 0,
    save() {
        localStorage.setItem('totalCatsSummoned', this.summons);
        localStorage.setItem('totalLegendaries', this.legendaries);
        localStorage.setItem('pityCounter', this.pity);
    }
};