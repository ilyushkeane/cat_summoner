import { personalities } from './personalities.js';

export function getRoll(state) {
    state.pity++;
    let pool;

    if (state.pity >= 20) {
        pool = personalities.filter(p => p.class === "legendary");
    } else {
        const roll = Math.random() * 100;
        if (roll < 5) pool = personalities.filter(p => p.class === "legendary");
        else if (roll < 20) pool = personalities.filter(p => p.class === "epic");
        else if (roll < 45) pool = personalities.filter(p => p.class === "rare");
        else pool = personalities.filter(p => p.class === "common");
    }

    const persona = pool[Math.floor(Math.random() * pool.length)];
    if (persona.class === 'legendary') state.pity = 0;
    
    return persona;
}