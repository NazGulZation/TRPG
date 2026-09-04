---
name: trpg-development
description: >-
  Develop, maintain, test, and expand the Dark Tragic Adult Text RPG web application
  (Ashen Solstice). Use when authoring new story chapters, designing NPCs with unique
  attributes (Sinew, Guile, Lucidity), configuring romance/intimacy mechanics,
  party recruitment, attack-on-sight hostility, factions, and testing Flask backend endpoints.
---

# Dark Tragic Adult Text RPG (TRPG) Development Skill

This skill provides guides, conventions, and procedures for extending the **Ashen Solstice** Dark Fantasy Text RPG engine and web application.

---

## 1. Project Architecture Overview

- **Python Environment**: Use `D:\Anaconda\python.exe`.
- **Backend**:
  - `app.py`: Flask web server with REST API (`/api/state`, `/api/action`). Runs by default on port `5050`.
  - `game/models.py`: Core domain data classes (`Stats`, `Player`, `NPC`, `Quest`, `QuestStage`, `Faction`, `Location`, `DialogueNode`, `DialogueChoice`).
  - `game/engine.py`: Game state manager handling travel, dialogue trees, stat checks, romance vignettes, party recruitment, attack-on-sight ambushes, dynamic quest progression, and tactical combat.
  - `game/data/prologue.py`: Content definitions for Prologue: "Ashen Solstice - The Sinking of Oakhaven".
- **Frontend**:
  - `templates/index.html`: Responsive gothic dark UI layout.
  - `static/css/style.css`: Grimdark theme, vital meters, combat arena, and styling.
  - `static/js/game.js`: Reactive game client handling async REST interaction.
- **Tests**:
  - `tests/test_trpg.py`: Unit and integration test suite covering engine mechanics, quests, dialogue checks, combat, and API routes.

---

## 2. Core Narrative & Design Guidelines

### Attributes System
Standard Strength / Agility / Intelligence are strictly replaced with:
1. **Sinew**: Muscular force, physical endurance, bodily resilience, raw intimidation.
2. **Guile**: Reflexes, stealth, precision strikes, sleight of hand, nimble evasion.
3. **Lucidity**: Mental fortitude, occult discernment, reading deceit, resistance to creeping dread and madness.

> [!IMPORTANT]
> Both the player and every NPC must possess explicit Sinew, Guile, and Lucidity values. Dialogue checks and combat outcomes compare player stats against NPC stats.

### Adult Romance & Courting Rules
- The protagonist is an **adult male**.
- Consenting adult characters (`can_romance: True`) can be courted **regardless of gender**.
- Intimate, mature vignettes unlock at high relationship (+75 or through special quest milestones), reducing Dread (restoring sanity) and cementing devotion.
- Non-combatants, traumatized elders, and minors (e.g. Little Toby) are **strictly non-romanceable** and non-combatants.

### Party Recruitment & Attack on Sight
- **Party Recruitment (+50 Relationship)**: Viable combatants (`is_combatant: True`) can join the player's warband (maximum 2 companions). Companions grant bonus damage in combat and assist in stat checks.
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
    can_romance=True, # Eligible adult
    dialogue_root="root",
    dialogue_nodes={...},
    loot=["Dawnbound Censer", "Executioner's Flail"]
)
```

### Adding Dialogue Nodes with Checks, Economy & Vignettes
```python
DialogueChoice(
    id="c_malik_confront",
    text="[Sinew 14] Slam him against the stone archway and demand answers.",
    next_node="malik_intimidated",
    required_stat="sinew",
    required_value=14,
    failure_node="malik_sinew_fail",
    relationship_change=10
)
```

For merchant or bribery transactions, set `sovereign_cost`:
```python
DialogueChoice(
    id="c_bribe_guard",
    text="Slip 25 Sovereigns to look the other way.",
    next_node="guard_bribed",
    sovereign_cost=25,
    relationship_change=5
)
```

For choices granting multiple items, use `item_rewards`:
```python
DialogueChoice(
    id="c_toby_take_key",
    text="Ruffle his hair gently. 'Hide in the hollow barrels until nightfall, Toby.'",
    next_node="toby_saved",
    item_rewards=["Master Sluice Key", "Turnkey's Stolen Ledger"],
    relationship_change=20
)
```

For intimate scenes:
```python
DialogueChoice(
    id="c_partner_intimacy",
    text="Embrace them behind the shadowed curtains, seeking warmth amidst the doom.",
    next_node="partner_intimate_scene",
    is_intimacy_action=True,
    relationship_change=25
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
   - Always use `engine.add_inventory_item(item_name)` when granting items (in dialogue choices, scavenge, combat loot, or quest rewards).
   - If an item satisfies an active quest stage (e.g., `"Wolfsbane Nectar"`, `"Loras's Iron Signet"`, `"Turnkey's Stolen Ledger"`), advance `quest.current_stage` and log a quest update automatically.
3. **Turn-In & Completion**:
   - When a completion choice is selected from `<npc>_quest_complete`, the engine marks the quest as `stage 99`, consumes any `required_item` from the player's inventory, distributes sovereign/item/faction rewards, and logs the completion.

### Prologue Climax & Escape Endings
Escape mechanics are triggered via `/api/action` (`escape` action) in `engine.attempt_escape(method)`:
- **`method="sluice_gate"`**: Requires the **Master Sluice Key** (acquired from Little Toby). Grants victory through the subterranean drainage canal.
- **`method="iron_gate"`**: Requires an **Imperial Transit Pass** (awarded by Madame Silve) or a **Silver Dawnshroud Seal** (awarded by Sister Vanya). Grants victory through the flaming Gallow-Gate.
- Triggering an escape sets `self.victory = True` and writes an apocalyptic victory narrative log to complete the chapter.

---

## 4. Verification and Execution Workflows

### Run the Automated Test Suite
Always verify engine integrity, dialogue paths, quest progressions, and combat turns before finalizing changes:
```powershell
$env:PYTHONPATH = "d:\Python\Project\TRPG"
& "D:\Anaconda\python.exe" -m unittest discover -s tests -p "test_*.py"
```

### Launch the Web App Server
```powershell
& "D:\Anaconda\python.exe" d:\Python\Project\TRPG\app.py
```
Default local URL: `http://127.0.0.1:5050`
