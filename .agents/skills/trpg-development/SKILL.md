---
name: trpg-development
description: >-
  Develop, maintain, test, and expand the Dark Tragic Adult Text RPG web application
  (Ashen Solstice). Use when authoring new story chapters, designing NPCs with unique
  attributes (Sinew, Guile, Lucidity), configuring heterosexual eroge romance/intimacy mechanics,
  interactive intimacy minigames, functional item mechanics, party recruitment, attack-on-sight hostility, factions, and testing Flask backend endpoints.
---

# Dark Tragic Adult Text RPG (TRPG) Development Skill

This skill provides guides, conventions, and procedures for extending the **Ashen Solstice** Dark Fantasy Eroge Text RPG engine and web application.

---

## 1. Project Architecture Overview

- **Python Environment**: Use `D:\Anaconda\python.exe`.
- **Backend**:
  - `app.py`: Flask web server with REST API (`/api/state`, `/api/action`). Handles travel, inspection, conversation, intimacy minigames (`intimacy_action`, `close_intimacy`), inventory activation (`use_item`), combat, and escape. Runs by default on port `5050`.
  - `game/models.py`: Core domain data classes (`Stats`, `Player`, `NPC`, `Quest`, `QuestStage`, `Faction`, `Location`, `DialogueNode`, `DialogueChoice`).
  - `game/engine.py`: Game state manager handling district traversal, dialogue trees, stat checks with item buffs, eroge intimacy minigame, party recruitment, attack-on-sight ambushes, functional item utility, dynamic quest progression, and tactical combat.
  - `game/data/prologue.py`: Content definitions for Prologue: "Ashen Solstice - The Sinking of Oakhaven".
- **Frontend**:
  - `templates/index.html`: Responsive gothic dark UI layout with vital meters, combat arena, eroge intimacy arena, dialogue overlay, and interactive haversack.
  - `static/css/style.css`: Grimdark theme, vital meters, intimacy minigame styling, combat arena, and atmospheric components.
  - `static/js/game.js`: Reactive game client handling async REST interaction, combat turns, item usage, and eroge intimacy minigame actions.
- **Tests**:
  - `tests/test_trpg.py`: Unit and integration test suite covering engine mechanics, quests, dialogue checks, eroge intimacy minigames, functional items, combat, and API routes.

---

## 2. Core Narrative & Design Guidelines

### Attributes System
Standard Strength / Agility / Intelligence are strictly replaced with:
1. **Sinew**: Muscular force, physical endurance, bodily resilience, raw intimidation, heavy blows in combat, and deep passionate physical rhythm.
2. **Guile**: Reflexes, stealth, precision strikes, sleight of hand, nimble evasion, precision weapon damage, and delicate erogenous touch.
3. **Lucidity**: Mental fortitude, occult discernment, reading deceit, resistance to creeping dread and madness, and emotional attunement/whispered worship.

> [!IMPORTANT]
> Both the player and every NPC must possess explicit Sinew, Guile, and Lucidity values. Dialogue checks, combat actions, and intimacy techniques compare player effective stats (including gear and companion bonuses) against difficulty targets.

### Eroge Romance & Heterosexual Courting Rules
- The protagonist is an **adult male**.
- Romance and erotic encounters are strictly **heterosexual** (only consenting **adult female** characters, e.g. Sister Vanya, Madame Silve, can be courted with `can_romance: True`).
- Male adult characters (e.g. Commander Malakor) feature a dedicated **Warrior Brotherhood & Blood-Oath** comrade dynamic (`can_romance: False`), earning battle respect, sparring in the pit, and sealing blood pacts.
- Non-combatants, traumatized elders, and minors (e.g. Little Toby) are **strictly non-romanceable** and non-combatants. Purely mentorship, survival guidance, and humanitarian protection.
- The game maintains a **50% tactical survival gameplay / 50% erotic scene & intimacy minigame** balance.

### Sensory Eroge Intimacy Minigame System
- Intimate encounters feature an interactive **Sensory Intimacy Minigame**:
  - **Partner Arousal Meter (0–100%)** built through interactive techniques tested against player attributes:
    - **[Guile Caress]**: Tactile stimulation beneath lace/linens (+25–35% Arousal).
    - **[Sinew Intensity]**: Commanding physical rhythm and deep kisses (+25–35% Arousal).
    - **[Lucidity Whisper]**: Whispered absolution, attunement to ragged breathing (+20–30% Arousal, -10 Dread, multiplies ecstasy rating).
    - **[Oral Devotion]**: Devoted oral worship (+35–45% Arousal).
  - Reaching 100% Arousal triggers the **Transcendent Ecstasy Climax**, completely wiping Dread to 0, setting relationship to 100/100, marking `is_romanced = True`, and awarding permanent relics.

### Zero Useless Items Policy
Every single item in the game possesses a concrete coded gameplay effect, stat buff, tool utility, consumable use, or quest role:
- **Relics / Keepsakes**:
  - `Sister Vanya's Embroidered Rosary`: +2 Lucidity in checks, halves Dread gain, usable to soothe 20 Dread.
  - `Silve's Scented Silk Favor`: +2 Guile in checks, permanent 25% discount on all sovereign costs and bribes.
  - `Malakor's Drake Whetstone`: +2 Sinew in checks, +4 flat physical damage to all player attacks in combat.
- **Consumables**:
  - `Spiced Plum Wine`: Restores 12 HP, soothes 15 Dread.
  - `Purified Bandage`: Restores 25 HP in combat or haversack.
  - `Torn Bandage`: Restores 18 HP in combat or haversack.
  - `Charred Rations`: Restores 8 HP or fed to Toby to gain his trust.
- **Tools & Keys**:
  - `Corroded Crowbar`: Pries open locked drainage sluices or mercenary supply chests.
  - `Tarnished Iron Nail`: Improvised lockpick for high gibbet cages in Gallow-Square.
  - `Chirurgeon Scalpel`: +3 precision damage weapon and surgical tool for patient triage.
  - `Master Sluice Key`, `Imperial Transit Pass`, `Silver Dawnshroud Seal`: Escape items triggering chapter victory.

### Party Recruitment & Attack on Sight
- **Party Recruitment (+50 Relationship)**: Viable combatants (`is_combatant: True`) can join the player's warband (maximum 2 companions). Companions grant bonus damage in combat and assist in stat checks (+1/4 companion stats).
- **Attack on Sight (<= -50 Relationship)**: When an NPC despises the player due to betrayal, insults, or faction warfare, moving into their sector immediately triggers an **Attack-on-Sight ambush** and initiates lethal combat.

---

## 3. How to Add and Extend Content

### Adding an NPC
Define in `game/data/<chapter>.py` using `NPC`:
```python
NPC(
    id="inquisitor_malik",
    name="Inquisitor Malik",
    title="The Pyre-Bearer",
    gender="male",
    faction_id="dawnshroud",
    description="A scarred zealot clad in blackened iron mail.",
    stats=Stats(sinew=15, guile=11, lucidity=14),
    max_hp=38,
    current_hp=38,
    relationship=-20,
    is_combatant=True,
    can_romance=False, # Male companion: warrior brotherhood only
    dialogue_root="root",
    dialogue_nodes={...},
    loot=["Dawnbound Censer", "Executioner's Flail"]
)
```

### Adding Dialogue Nodes with Checks, Economy & Erotic Minigames
```python
DialogueChoice(
    id="c_partner_minigame_start",
    text="Engage in the 'Sanctum of the Flesh' Intimacy Minigame.",
    next_node="partner_eroge_minigame_start",
    is_intimacy_action=True,
    relationship_change=20
)
```

For merchant or bribery transactions with automatic silk discount:
```python
DialogueChoice(
    id="c_bribe_guard",
    text="Slip 25 Sovereigns to look the other way.",
    next_node="guard_bribed",
    sovereign_cost=25,
    relationship_change=5
)
```

### Dynamic Dialogue Routing Conventions in `talk_npc()`
When an NPC conversation starts via `engine.talk_npc(npc_id)`, the dialogue node is dynamically routed in the following precedence:
1. **Attack on Sight Ambush**: If `npc.relationship <= -50`, conversation is aborted and lethal combat initiates immediately (`ambush=True`).
2. **Turn-In Node (`<npc>_quest_complete`)**: If the player possesses the quest's required item (e.g., `Wolfsbane Nectar`, `Loras's Iron Signet`, `Turnkey's Stolen Ledger`), route directly to the turn-in node and advance the quest stage to 2.
3. **Completed Quest Node**: If `quest.current_stage == 99`, load the post-quest state rather than resetting to `root`.
4. **Active Quest Reminder (`<npc>_quest_accepted`)**: If `quest.current_stage == 1` and the player does not yet possess the item, load the reminder node rather than repeating the initial greeting.
5. **State-Based Fled/Resolved Routing**: For transient NPCs (such as Little Toby), route to their persistent aftermath nodes (`toby_saved` or `toby_robbed`) based on disposition to prevent loop exploits.
6. **Default Fallback**: `npc.dialogue_root` ("root").

### Quest Lifecycle and Inventory Integration
1. **Stages & Objectives**:
   - `stage_id = 0`: Not started.
   - `stage_id = 1+`: Active quest objectives with `target_location`, `target_npc`, and optional `required_item`.
   - `stage_id = 99`: Completed.
2. **Item Acquisition Hook**:
   - Always use `engine.add_inventory_item(item_name)` when granting items.
   - If an item satisfies an active quest stage, advance `quest.current_stage` and log a quest update automatically.
3. **Turn-In & Completion**:
   - When a completion choice is selected from `<npc>_quest_complete`, mark quest stage as `99`, consume any `required_item`, distribute rewards, and log completion.

---

## 4. Verification and Execution Workflows

### Run the Automated Test Suite
Always verify engine integrity, dialogue paths, quest progressions, eroge intimacy minigames, and combat turns before finalizing changes:
```powershell
$env:PYTHONPATH = "d:\Python\Project\TRPG"
& "D:\Anaconda\python.exe" -m unittest discover -s tests -p "test_*.py"
```

### Launch the Web App Server
```powershell
& "D:\Anaconda\python.exe" d:\Python\Project\TRPG\app.py
```
Default local URL: `http://127.0.0.1:5050`
