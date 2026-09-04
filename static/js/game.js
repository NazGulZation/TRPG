/**
 * Dark Tragic Adult Text RPG - Game Client
 */

const GameApp = {
    state: null,

    async init() {
        document.getElementById('btn-reset').addEventListener('click', () => this.resetGame());
        await this.fetchState();
    },

    async fetchState() {
        try {
            const resp = await fetch('/api/state');
            const data = await resp.json();
            this.state = data;
            this.render();
        } catch (e) {
            console.error("Failed to load state", e);
        }
    },

    async sendAction(payload) {
        try {
            const resp = await fetch('/api/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            if (data.error) {
                alert(data.error);
                return;
            }
            this.state = data;
            this.render();
        } catch (e) {
            console.error("Action error", e);
        }
    },

    travel(destId) {
        this.sendAction({ action: 'travel', destination_id: destId });
    },

    inspectGround() {
        this.sendAction({ action: 'inspect' });
    },

    talkNpc(npcId) {
        this.sendAction({ action: 'talk', npc_id: npcId });
    },

    chooseDialogue(choiceId) {
        this.sendAction({ action: 'dialogue_choice', choice_id: choiceId });
    },

    closeDialogue() {
        this.sendAction({ action: 'close_dialogue' });
    },

    recruit(npcId) {
        this.sendAction({ action: 'recruit', npc_id: npcId });
    },

    dismiss(npcId) {
        this.sendAction({ action: 'dismiss', npc_id: npcId });
    },

    startEroticScene(npcId) {
        this.sendAction({ action: 'start_erotic_scene', npc_id: npcId });
    },

    combatAction(type) {
        this.sendAction({ action: 'combat_action', combat_type: type });
    },

    intimacyAction(type) {
        this.sendAction({ action: 'intimacy_action', technique: type });
    },

    closeIntimacy() {
        this.sendAction({ action: 'close_intimacy' });
    },

    useItem(itemName) {
        this.sendAction({ action: 'use_item', item_name: itemName });
    },

    attemptEscape(method) {
        this.sendAction({ action: 'escape', method: method });
    },

    resetGame() {
        if (confirm("Abandon your journey and awaken again in the ash?")) {
            this.sendAction({ action: 'reset' });
        }
    },

    render() {
        if (!this.state) return;

        const { player, location, factions, active_quests, dialogue, combat, logs, game_over, victory } = this.state;

        // Bell Ticker
        const bellToll = this.state.bell_toll || 9;
        const hoursLeft = 12 - bellToll;
        const bellTickerEl = document.getElementById('bell-ticker');
        if (bellTickerEl) {
            if (bellToll >= 12) {
                bellTickerEl.textContent = 'BELL: 12:00 MIDNIGHT (PURGE COMMENCED)';
                bellTickerEl.style.color = '#ff3333';
            } else {
                bellTickerEl.textContent = `BELL: ${bellToll}:00 PM (${hoursLeft}h to Midnight)`;
                bellTickerEl.style.color = '';
            }
        }

        // Player Vitals & Stats
        document.getElementById('p-name').textContent = player.name;
        document.getElementById('p-title').textContent = `${player.title} (${player.gender.toUpperCase()})`;
        
        const hpPct = Math.max(0, Math.min(100, (player.hp / player.max_hp) * 100));
        document.getElementById('p-hp-bar').style.width = `${hpPct}%`;
        document.getElementById('p-hp-text').textContent = `${player.hp}/${player.max_hp}`;

        const dreadPct = Math.max(0, Math.min(100, player.dread));
        document.getElementById('p-dread-bar').style.width = `${dreadPct}%`;
        document.getElementById('p-dread-text').textContent = `${player.dread}/100`;

        document.getElementById('stat-sinew').textContent = player.stats.sinew;
        document.getElementById('stat-guile').textContent = player.stats.guile;
        document.getElementById('stat-lucidity').textContent = player.stats.lucidity;

        document.getElementById('p-sovereigns').textContent = player.sovereigns;

        // Party List
        const partyListEl = document.getElementById('party-list');
        document.getElementById('party-count').textContent = `${player.party.length}/2`;
        if (player.party.length === 0) {
            partyListEl.innerHTML = `<p class="empty-note">No companions sworn to your side. Form bonds or recruit capable warriors.</p>`;
        } else {
            partyListEl.innerHTML = player.party.map(c => `
                <div class="party-member-card ${c.is_romanced ? 'romanced' : ''}">
                    <div class="party-member-header">
                        <span>${c.is_romanced ? '&#9829; ' : ''}${c.name}</span>
                        <span class="companion-title">${c.title || ''}</span>
                    </div>
                    <div class="party-stats">
                        HP: ${c.hp}/${c.max_hp} | S:${c.stats.sinew} G:${c.stats.guile} L:${c.stats.lucidity}
                    </div>
                    <div class="party-member-actions">
                        <button class="btn-sm btn-party-talk" onclick="GameApp.talkNpc('${c.id}')">Talk</button>
                        ${c.can_romance && c.gender === 'female' ? `
                            <button class="btn-sm btn-party-erotic" onclick="GameApp.startEroticScene('${c.id}')">&#9829; Erotic Scene</button>
                        ` : ''}
                        <button class="btn-sm btn-party-dismiss" onclick="GameApp.dismiss('${c.id}')">Dismiss</button>
                    </div>
                </div>
            `).join('');
        }

        // Faction Meters
        const factionListEl = document.getElementById('faction-list');
        factionListEl.innerHTML = Object.entries(factions).map(([fid, fmeta]) => {
            const rep = player.factions[fid] || 0;
            const sign = rep > 0 ? `+${rep}` : `${rep}`;
            const pct = Math.max(0, Math.min(100, (rep + 50)));
            return `
                <div class="faction-item" title="${fmeta.desc}">
                    <div class="faction-item-header">
                        <span style="color: ${fmeta.color}; font-weight: 600;">${fmeta.name}</span>
                        <span>${sign}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="fill" style="width: ${pct}%; background: ${fmeta.color};"></div>
                    </div>
                </div>
            `;
        }).join('');

        // Location & Travel Deck
        document.getElementById('loc-name').textContent = location.name;
        document.getElementById('loc-subtitle').textContent = location.subtitle;
        
        const dangerEl = document.getElementById('loc-danger');
        dangerEl.textContent = `SECTOR: ${location.faction_id.toUpperCase()}`;

        const travelBtnsEl = document.getElementById('travel-buttons');
        travelBtnsEl.innerHTML = location.connected.map(c => `
            <button class="btn-action" onclick="GameApp.travel('${c.id}')">&#10148; ${c.name}</button>
        `).join('');

        // Escape Buttons Check
        const btnSluice = document.getElementById('btn-escape-sluice');
        const btnGate = document.getElementById('btn-escape-gate');
        if (location.id === 'sluice_trench') {
            btnSluice.classList.remove('hidden');
        } else {
            btnSluice.classList.add('hidden');
        }
        if (location.id === 'iron_bastion' || location.id === 'gallow_square') {
            btnGate.classList.remove('hidden');
        } else {
            btnGate.classList.add('hidden');
        }

        // Local NPCs
        const npcListEl = document.getElementById('npc-list');
        if (!location.npcs || location.npcs.length === 0) {
            npcListEl.innerHTML = `<p class="empty-note">No one lingers in this desolate corner.</p>`;
        } else {
            npcListEl.innerHTML = location.npcs.map(npc => {
                let relClass = 'rel-mid';
                let relDesc = 'Neutral';
                if (npc.relationship >= 50) { relClass = 'rel-high'; relDesc = 'Devoted'; }
                else if (npc.relationship >= 20) { relClass = 'rel-high'; relDesc = 'Friendly'; }
                else if (npc.relationship <= -50) { relClass = 'rel-hostile'; relDesc = 'Hostile (KOS)'; }
                else if (npc.relationship < 0) { relClass = 'rel-hostile'; relDesc = 'Distrustful'; }

                let romanceTag = npc.is_romanced ? '<span style="color: #ff4081;">&#9829; Lover</span>' : '';
                let canRecruit = npc.is_combatant && npc.relationship >= 50 && player.party.length < 2;

                return `
                    <div class="npc-card">
                        <div class="npc-card-header">
                            <span class="npc-name">${npc.name}</span>
                            <span class="npc-rel-badge ${relClass}">${npc.relationship} (${relDesc})</span>
                        </div>
                        <div class="sub-title">${npc.title} ${romanceTag}</div>
                        <p class="npc-card-desc">${npc.description}</p>
                        <div class="npc-stats-line">
                            Sinew: ${npc.stats.sinew} | Guile: ${npc.stats.guile} | Lucidity: ${npc.stats.lucidity}
                        </div>
                        <div class="npc-actions-row">
                            <button class="btn-sm" onclick="GameApp.talkNpc('${npc.id}')">Converse</button>
                            ${canRecruit ? `<button class="btn-sm" style="border-color: #55bb77;" onclick="GameApp.recruit('${npc.id}')">+ Recruit</button>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Active Quests
        const questListEl = document.getElementById('quest-list');
        if (active_quests.length === 0) {
            questListEl.innerHTML = `<p class="empty-note">No active vows or quests.</p>`;
        } else {
            questListEl.innerHTML = active_quests.map(q => `
                <div class="quest-item">
                    <div class="quest-title">&#9872; ${q.title}</div>
                    <div class="quest-desc">${q.stage_description || q.description}</div>
                </div>
            `).join('');
        }

        // Inventory
        const invListEl = document.getElementById('inventory-list');
        document.getElementById('inv-count').textContent = `${player.inventory.length} items`;
        const usableItems = [
            "Spiced Plum Wine", "Purified Bandage", "Torn Bandage", "Charred Rations",
            "Corroded Crowbar", "Tarnished Iron Nail", "Sister Vanya's Embroidered Rosary",
            "Malakor's Drake Whetstone", "Silve's Scented Silk Favor"
        ];
        invListEl.innerHTML = player.inventory.map(item => {
            const isUsable = usableItems.includes(item);
            return `
                <li class="inv-item ${isUsable ? 'inv-item-usable' : ''}">
                    <span>&#9671; ${item}</span>
                    ${isUsable ? `<button class="inv-btn-use" onclick="GameApp.useItem('${item}')">Use</button>` : ''}
                </li>
            `;
        }).join('');

        // Narrative Scroll
        const logEl = document.getElementById('narrative-log');
        logEl.innerHTML = logs.map(l => `
            <div class="log-entry ${l.category}">
                <div class="log-title">${l.title}</div>
                <div class="log-text">${l.text}</div>
            </div>
        `).join('');
        logEl.scrollTop = logEl.scrollHeight;

        // Dialogue Box
        const diagBox = document.getElementById('dialogue-box');
        if (dialogue) {
            diagBox.classList.remove('hidden');
            document.getElementById('diag-speaker').textContent = dialogue.speaker;
            document.getElementById('diag-title').textContent = dialogue.npc_title;
            document.getElementById('diag-text').textContent = dialogue.text;
            
            const choicesEl = document.getElementById('diag-choices');
            if (dialogue.choices && dialogue.choices.length > 0) {
                choicesEl.innerHTML = dialogue.choices.map(c => {
                    let cls = 'dialogue-btn';
                    if (c.is_intimacy || c.is_romance) cls += ' romance';
                    if (c.is_hostile) cls += ' hostile';
                    let disabled = (!c.stat_met || !c.item_met || (c.sovereigns_met === false)) ? 'disabled' : '';
                    let note = '';
                    if (!c.stat_met) note += ' [Stat Unmet]';
                    if (!c.item_met) note += ' [Missing Item]';
                    if (c.sovereigns_met === false) note += ' [Need Sovereigns]';
                    return `
                        <button class="${cls}" ${disabled} onclick="GameApp.chooseDialogue('${c.id}')">
                            ${c.text}${note}
                        </button>
                    `;
                }).join('');
            } else {
                choicesEl.innerHTML = `<button class="dialogue-btn" onclick="GameApp.closeDialogue()">Conclude conversation</button>`;
            }
        } else {
            diagBox.classList.add('hidden');
        }

        // Combat Arena
        const combatArena = document.getElementById('combat-arena');
        if (combat) {
            combatArena.classList.remove('hidden');
            document.getElementById('combat-enemy-name').textContent = `${combat.npc_name} (Round ${combat.turn})`;
            const eHpPct = Math.max(0, Math.min(100, (combat.npc_hp / combat.npc_max_hp) * 100));
            document.getElementById('combat-enemy-hp-fill').style.width = `${eHpPct}%`;
            document.getElementById('combat-enemy-hp-text').textContent = `${combat.npc_hp}/${combat.npc_max_hp} HP`;

            const combatLogEl = document.getElementById('combat-log');
            combatLogEl.innerHTML = combat.combat_log.map(line => `<div>${line}</div>`).join('');
            combatLogEl.scrollTop = combatLogEl.scrollHeight;
        } else {
            combatArena.classList.add('hidden');
        }


        // End Game Modal
        const modal = document.getElementById('endgame-modal');
        if (game_over) {
            modal.classList.remove('hidden');
            document.getElementById('modal-title').textContent = "YOU HAVE PERISHED";
            document.getElementById('modal-body').innerHTML = `
                <p>The darkness of Oakhaven has consumed you. Your remains are cast into the sulfur trenches along with thousands of other forgotten souls.</p>
            `;
        } else if (victory) {
            modal.classList.remove('hidden');
            document.getElementById('modal-title').textContent = "SURVIVED THE PURGE";
            document.getElementById('modal-body').innerHTML = `
                <p>As the white phosphorus rain consumes Oakhaven in a blazing inferno behind you, you reach the safety of the outer mist with your sworn allies.</p>
                <p>You have conquered the Prologue Chapter: <em>Ashen Solstice - The Sinking of Oakhaven</em>.</p>
            `;
        } else {
            modal.classList.add('hidden');
        }
    }
};

window.addEventListener('DOMContentLoaded', () => {
    GameApp.init();
});
