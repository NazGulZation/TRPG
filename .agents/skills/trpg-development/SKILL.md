---
name: trpg-development
description: >-
  Develop, maintain, test, and expand adult eroge text RPG web applications. Use
  when authoring story chapters, designing NPCs and attribute systems,
  configuring SQLite chapter content, heterosexual eroge romance, writing lengthy
  explicit narrative erotic scenes (without redundant minigames, with unique
  steps 4-10 branch progression and step 1 decline/leave options), implementing
  party companion interactions (dialogue hubs and intimacy initiation), party
  recruitment constraints, max party capacity, save/load/continue persistence,
  functional items, hostility mechanics, factions, and testing modular Flask and
  engine components.
---

# Adult Eroge Text RPG Development Skill

This skill provides comprehensive conventions, architectural patterns, narrative guidelines, data schemas, and testing procedures for authoring and expanding **Adult Eroge Text RPG** web applications.

---

## 1. Architectural Patterns & Technical Foundation

### Core Stack
- **Backend**: Python with Flask providing a session-driven REST API (`/api/state`, `/api/action`, `/api/save`, `/api/load`, `/api/saves`, `/api/continue`).
- **Engine Core**: Pure Python domain layer decoupled from HTTP concerns.
  - `models.py`: Dataclasses with `from_dict` and `to_dict` serialization for Player, Stats, NPC, Quest, Faction, Location, DialogueNode, DialogueChoice, Item.
  - `engine.py`: Central state machine handling location traversal, dynamic dialogue resolution, attribute checks with gear/companion buffs, multi-stage explicit erotic encounters, party recruitment, companion dialogue hubs, faction hostility, inventory management, tactical turn-based combat, and disk/dict game state save/load serialization.
  - **SQLite Game Data Architecture** (`game/data/game_data.db` & `game/data/db.py`): All chapter-specific configuration data (locations, factions, quests, NPCs, dialogues, metadata, items) is stored in relational SQLite tables rather than scattered JSON files or monolithic Python dictionaries. Python loader modules (`game/data/<chapter>.py`) query `game_data.db` using `get_db_connection()` to instantiate typed dataclass models.
- **Frontend**: Lightweight, reactive single-page client (HTML5, CSS3, vanilla JavaScript).
  - Narrative chronicle displaying environmental prose and event history.
  - Interactive dialogue choice overlays.
  - Vitals, stats, and status meters (Health, Morale/Dread, Stamina, Sovereigns/Currency).
  - Interactive inventory / haversack with usable items.
  - Companion / Warband roster with dedicated quick-action controls (`[Talk]`, `[♥ Erotic Scene]`, `[Dismiss]`).
  - Modal system for Save Game, Load Game, and Continue flows.
- **Testing Architecture**:
  - Test suites organized by system layer and chapter scope under `tests/` and `tests/<chapter>/`.

---

## 2. Chapter Data Architecture (SQLite Database)

All configurable chapter content is unified into a relational SQLite database located at `game/data/game_data.db`, accessed through the helper module `game/data/db.py`:

```
game/data/
├── game_data.db            # SQLite database containing all relational tables
├── db.py                   # DB connection helper (get_db_connection)
└── <chapter_id>.py         # Typed chapter loader module (e.g. prologue.py)
```

### 1. Database Schema
The database contains seven core relational tables:
- `metadata`: `(chapter_id TEXT PRIMARY KEY, title TEXT, opening_category TEXT, opening_title TEXT, opening_text TEXT, suitable_intimacy_locations TEXT)`
- `factions`: `(chapter_id TEXT, faction_id TEXT, name TEXT, desc TEXT, color TEXT, PRIMARY KEY (chapter_id, faction_id))`
- `items`: `(chapter_id TEXT, item_id TEXT, name TEXT, description TEXT, item_type TEXT, is_usable INTEGER, effect_type TEXT, effect_value INTEGER, effect_description TEXT, PRIMARY KEY (chapter_id, item_id))`
- `locations`: `(chapter_id TEXT, location_id TEXT, name TEXT, subtitle TEXT, description TEXT, faction_id TEXT, connected_locations TEXT, npc_ids TEXT, items_on_ground TEXT, danger_level INTEGER, PRIMARY KEY (chapter_id, location_id))`
- `quests`: `(chapter_id TEXT, quest_id TEXT, title TEXT, description TEXT, giver_npc_id TEXT, faction_id TEXT, current_stage INTEGER, stages TEXT, reward_items TEXT, reward_sovereigns INTEGER, reward_relation INTEGER, reward_faction_points INTEGER, completion_text TEXT, PRIMARY KEY (chapter_id, quest_id))`
- `npcs`: `(chapter_id TEXT, npc_id TEXT, name TEXT, title TEXT, gender TEXT, faction_id TEXT, description TEXT, stats TEXT, max_hp INTEGER, current_hp INTEGER, relationship INTEGER, is_combatant INTEGER, can_romance INTEGER, can_recruit INTEGER, is_in_party INTEGER, is_romanced INTEGER, is_dead INTEGER, dialogue_root TEXT, active_quest_id TEXT, loot TEXT, PRIMARY KEY (chapter_id, npc_id))`
- `dialogues`: `(chapter_id TEXT, npc_id TEXT, node_id TEXT, speaker_name TEXT, text TEXT, choices TEXT, PRIMARY KEY (chapter_id, npc_id, node_id))`

### 2. Chapter Loader Pattern (`game/data/<chapter>.py`)
Python chapter modules query `game_data.db` and instantiate typed dataclasses:
```python
import json
from game.models import Location, NPC, Quest, DialogueNode, DialogueChoice, Item
from game.data.db import get_db_connection

def get_prologue_items() -> dict[str, Item]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM items WHERE chapter_id = 'prologue'").fetchall()
    conn.close()
    items = {}
    for row in rows:
        item = Item(
            id=row["item_id"],
            name=row["name"],
            description=row["description"] or "",
            item_type=row["item_type"] or "quest",
            is_usable=bool(row["is_usable"]),
            effect_type=row["effect_type"],
            effect_value=row["effect_value"] or 0,
            effect_description=row["effect_description"] or "",
        )
        items[item.id] = item
        items[item.name] = item
    return items

def get_prologue_npcs() -> dict[str, NPC]:
    conn = get_db_connection()
    npc_rows = conn.execute("SELECT * FROM npcs WHERE chapter_id = 'prologue'").fetchall()
    dialogue_rows = conn.execute("SELECT * FROM dialogues WHERE chapter_id = 'prologue'").fetchall()
    conn.close()

    dialogues_by_npc = {}
    for d in dialogue_rows:
        npc_id = d["npc_id"]
        node_id = d["node_id"]
        choices_raw = json.loads(d["choices"] or "[]")
        node_obj = DialogueNode.from_dict({
            "id": node_id,
            "speaker_name": d["speaker_name"],
            "text": d["text"],
            "choices": choices_raw,
        })
        if npc_id not in dialogues_by_npc:
            dialogues_by_npc[npc_id] = {}
        dialogues_by_npc[npc_id][node_id] = node_obj

    npcs = {}
    for row in npc_rows:
        npc_id = row["npc_id"]
        npc_data = {
            "id": npc_id,
            "name": row["name"],
            "title": row["title"] or "",
            "gender": row["gender"] or "other",
            "faction_id": row["faction_id"] or "",
            "description": row["description"] or "",
            "stats": json.loads(row["stats"] or "{}"),
            "max_hp": row["max_hp"] or 30,
            "current_hp": row["current_hp"] or 30,
            "relationship": row["relationship"] or 0,
            "is_combatant": bool(row["is_combatant"]),
            "can_romance": bool(row["can_romance"]),
            "can_recruit": bool(row["can_recruit"]),
            "is_in_party": bool(row["is_in_party"]),
            "is_romanced": bool(row["is_romanced"]),
            "is_dead": bool(row["is_dead"]),
            "dialogue_root": row["dialogue_root"] or "root",
            "active_quest_id": row["active_quest_id"],
            "loot": json.loads(row["loot"] or "[]"),
        }
        npcs[npc_id] = NPC.from_dict(npc_data, dialogue_nodes=dialogues_by_npc.get(npc_id, {}))
    return npcs
```

---

## 3. Party Recruitment Constraints & Capacity

### Selective Recruitment (`can_recruit`)
Not every ally, merchant, commander, or companion can be recruited into the traveling warband:
1. **Explicit Flag (`can_recruit: bool`)**:
   - Every NPC must explicitly define `can_recruit`.
   - Characters who have other duties (e.g. Commander Malakor commanding his garrison, Madame Silve managing her den) or dependents/minors (Little Toby) must have `can_recruit: false`.
   - In Prologue, only Sister Vanya has `can_recruit: true`.
2. **Dialogue Pruning**:
   - Do **NOT** include recruitment or invitation dialogue choices (e.g. `"Join my travels"`, `c_malakor_recruit`) for characters with `can_recruit: false`.
3. **Engine Enforcement**:
   - `engine.recruit_party(npc_id)` checks `if not npc.can_recruit: return {"error": f"'{npc.name}' cannot be recruited into your party."}`.
4. **Party Capacity (Max 4)**:
   - Warband capacity is capped at 4 companions (`max_party_size = 4`).
   - If the player attempts to recruit when `len(self.player.party) >= self.max_party_size`, the engine returns `{"error": "Party is full (maximum 4 companions)."}`.

---

## 4. Save, Load, and Continue System

### State Serialization
The game engine supports full round-trip serialization of player attributes, quest progress, companion rosters, relationship values, and sector states:
- `engine.save_to_dict() -> dict`: Serializes player, inventory, stats, factions, quests, NPCs, locations, bell toll, and flags.
- `engine.load_from_dict(data: dict) -> bool`: Restores engine state completely.
- `engine.save_to_file(slot_name: str) -> str`: Persists state to `saves/<slot_name>.json` with ISO timestamp metadata.
- `engine.load_from_file(slot_name: str) -> bool`: Loads state from file.

### REST API Endpoints
- `POST /api/save`: Payload `{"slot": "save_slot_1"}` -> Saves current session state.
- `GET /api/saves`: Returns JSON list of save files sorted by modification time (`slot`, `filename`, `timestamp`, `player_name`, `location`, `hp`, `sovereigns`).
- `POST /api/load`: Payload `{"slot": "save_slot_1"}` -> Loads saved state into current session.
- `POST /api/continue`: Automatically discovers and loads the most recently modified save file.

---

## 5. Narrative & Eroge Design Principles

### Balance of Gameplay and Intimacy
Maintain a **50% gameplay / 50% erotic romance** balance:
- The game is a fully realized tactical RPG with survival, exploration, combat, questing, and consequences.
- Erotic encounters are meaningful narrative milestones and emotional payoffs, not hollow isolated minigames.

### Heterosexual Romance & Companion Archetypes
1. **Adult Male Protagonist**: The narrative centers on an adult male protagonist.
2. **Consenting Adult Female Romanceable Characters (`can_romance: True`)**:
   - Romance and erotic encounters are strictly heterosexual and involve consenting adult female characters.
   - Built on affection, shared hardship, emotional vulnerability, and mutual respect.
   - High relationship/devotion unlocks dedicated intimate scenes, companion abilities, and party loyalty.
3. **Male Companions & Comrades (`can_romance: False`)**:
   - Male companions feature a dedicated **Warrior Brotherhood & Camaraderie** dynamic.
   - Character arcs focus on battlefield trust, sparring, shared rations or drinks, oaths of loyalty, and tactical coordination.
4. **Protection of Innocents & Minors**:
   - Non-combatant elders, dependents, or minor NPCs are strictly **non-romanceable** and non-combatants.
   - Interactions are strictly focused on mentorship, protection, rescue, and humanitarian relief.

---

## 6. Lengthy Explicit Narrative Erotic Scenes

### Elimination of Redundant Minigames
- Avoid mechanical intimacy mini-games (arousal bars, stamina friction gauges, rhythm QTEs, technique check loops). They disrupt narrative immersion.
- All intimate encounters flow naturally through **rich, multi-stage narrative dialogue trees**.

### The 10-Step Narrative Progression & Unique Branch Paths
Structure major erotic sequences into continuous, richly descriptive 10-node progressions. Crucially, **each foreplay branch must maintain its own unique narrative nodes from Step 4 through Step 10 Climax and Afterglow** without merging into shared mid-scene nodes.

1. **Step 1: Initiating & Voluntary Retreat** (`<npc>_<loc>_step1_initiate` / `<npc>_intimacy_scene`):
   - Private retreat, atmospheric immersion, emotional vulnerability, and shedding armor/garments.
   - **Step 1 Decline / Leave Option**: The player must always have an explicit choice to pause, decline, or step back before committing to intimacy (e.g. returning to the companion hub or quest completion node).
   - **Deferred Intimacy Flags**: Step 1 entry and continuation choices must set `"is_intimacy_action": false`. Intimacy flags (`is_romanced = True`, Dread reduction to 0, keepsake rewards) must only trigger upon reaching the Step 10 Climax.
2. **Step 2: Sensual Foreplay & Branching Choices** (`<npc>_<loc>_step2_foreplay`):
   - At least 3 distinct narrative choices (e.g., Tender Romance, Dominant Passion, Devoted Oral / Sensory Indulgence).
3. **Step 3: Deepening Foreplay & Sensory Reaction** (`<npc>_<loc>_step3_<branch>`):
   - Visceral physical and vocal reactions to the chosen branch (flushed skin, wanton gasps, trembling thighs, lubrication).
4. **Step 4: Intimate Caresses & Lubrication** (`<npc>_<loc>_<branch>_step4_caress`):
   - Tactile exploration, parting thighs, and spreading natural lubrication tailored to the branch's tone.
5. **Step 5: Penetration & Alignment** (`<npc>_<loc>_<branch>_step5_entry`):
   - Deliberate, explicit description of penetration: alignment, stretching snug walls, taking full length to the root.
6. **Step 6: Initial Cadence & Deep Friction** (`<npc>_<loc>_<branch>_step6_rhythm`):
   - Finding the rhythm, internal friction, suction, and breathless shared gasps unique to the chosen position.
7. **Step 7: Positional Shift & Escalation** (`<npc>_<loc>_<branch>_step7_shift`):
   - Altering posture, angles, or elevation to target sensitive nerve centers with wet rhythmic impacts.
8. **Step 8: Fierce Cadence & Vocal Surrender** (`<npc>_<loc>_<branch>_step8_frenzy`):
   - Relentless strokes, sweat-sheened skin, and uninhibited wanton cries drowning out external noise.
9. **Step 9: The Precipice (Edging / Pre-Climax)** (`<npc>_<loc>_<branch>_step9_precipice`):
   - Involuntary passage spasms, desperate clutching, frantic breathing, and mutual surrender on the brink.
10. **Step 10: Explosive Climax** (`<npc>_<loc>_<branch>_step10_climax`):
    - Mutual, overwhelming orgasmic release: internal flooding, violent contractions, vocal release, and total surrender.
    - Set `"is_intimacy_action": true` on the Climax / Afterglow transition choice.
    - **Tangible Gameplay Rewards**:
      - Complete purge of negative mental states (Dread, Stress, or Insanity reset to 0).
      - Full devotion / relationship set to maximum (100).
      - Character marked as `is_romanced = True`.
      - Awarding unique permanent relics, accessories, or romantic perks.

- **Afterglow & Bonding** (`<npc>_<loc>_afterglow` or `<npc>_<loc>_<branch>_afterglow`):
  - Quiet, lingering embrace, shared warmth, and emotional pillow talk.
  - Smooth narrative transition back to companion traveling hub (`<npc>_companion_hub`) or party recruitment (`<npc>_recruited`).

### Location Suitability Gating & Location-Unique Scenes
Intimacy requires seclusion, privacy, and atmospheric comfort. Companions will not engage in carnal intimacy in exposed, public, or hostile zones (e.g., gibbet squares, crowded mercenary yards, toxic sewer trenches):
1. **Suitability Mapping (`SUITABLE_INTIMACY_LOCATIONS`)**:
   - Maintain a dictionary mapping each romanceable NPC to their allowed sector IDs:
     ```python
     SUITABLE_INTIMACY_LOCATIONS = {
         "sister_vanya": ["ruined_chantry", "gilded_rat"],
         "madame_silve": ["gilded_rat"]
     }
     ```
   - Unrecruitable characters who never leave their home base must only map to their home district (e.g. Madame Silve only at `gilded_rat`).
2. **Starting Location as Default Scene**:
   - The character's home district hosts their default erotic sequence (e.g., Sister Vanya in the sanctified crypt of the Ruined Chantry; Madame Silve in her velvet boudoir at the Gilded Rat).
3. **Location-Unique Intimate Narratives**:
   - Traveling to other suitable havens unlocks completely distinct 10-step erotic scenes reflecting environmental contrast (e.g., pious nun yielding to luxury on opium-scented crimson silks).
4. **Companion Dialogue Hub Gating**:
   - In `<npc>_companion_hub`, choices with `is_intimacy_action = True` are hidden dynamically unless `can_initiate_companion_erotic(npc_id)` evaluates to `True`.
5. **Direct Erotic Scene Dispatch**:
   - `start_party_erotic_scene(npc_id)` verifies `can_initiate_companion_erotic(npc_id)`. If in an unsuitable sector, returns an immersive error guiding the player to seek a secluded haven.

---

## 7. Modular Test Architecture

Tests are strictly divided into **System/Core Level** and **Chapter-Scoped** directories to maintain clean isolation, fast iteration, and zero clutter:

```
tests/
├── test_trpg.py                         # Backward-compatible runner & aggregator (load_tests)
├── test_engine_core.py                  # System: state initialization, travel, dice checks, combat, item effects
├── test_save_load.py                    # System: serialization, disk file persistence, save/load/continue APIs
├── test_api.py                          # System: Flask HTTP API routes and session handling
├── test_database.py                     # System: SQLite schema, table counts, dialogue referential integrity
└── <chapter_id>/                        # Chapter-Scoped Tests (e.g. tests/prologue/)
    ├── __init__.py
    ├── test_data_integrity.py           # Chapter: SQLite schema validation & dialogue tree graph integrity
    ├── test_quests.py                   # Chapter: storyline quests and branching outcomes
    ├── test_companions_and_intimacy.py  # Chapter: companion hubs, intimacy scenes, and location suitability
    └── test_party_recruitment.py        # Chapter: recruitment rules, unrecruitable allies, party capacity
```

### Test Execution Commands
- **Run All Tests (All Chapters & Systems)**:
  ```powershell
  python -m unittest discover -s tests -p "test_*.py"
  ```
- **Run Specific Chapter Tests Only**:
  ```powershell
  python -m unittest discover -s tests/prologue -p "test_*.py"
  ```
- **Run Direct Test Runner Aggregator**:
  ```powershell
  python -m unittest tests/test_trpg.py
  ```

---

## 8. Development & Verification Checklist

- [ ] **SQLite Data Architecture**: Story, dialogue trees, NPC profiles, locations, quests, and items reside in `game/data/game_data.db`, queried via `game/data/db.py`, not hardcoded Python dicts or raw JSON files.
- [ ] **Items Configuration & Anti-Bloat**: Items are defined in the `items` table using `Item` dataclasses. Filler consumable bloat is eliminated in favor of quest items, escape keys, and romance/brotherhood relics.
- [ ] **Dialogue Integrity**: Dialogue graphs in the `dialogues` table validated: every `next_node` and `failure_node` targets an existing node with no broken links.
- [ ] **Recruitment Constraints**: Non-recruitable characters have `can_recruit: 0/false`, have no party invitation choices in dialogues, and cannot be recruited via API.
- [ ] **Party Cap**: Max party size of 4 is respected across engine, API, and UI.
- [ ] **Save / Load Integrity**: All newly introduced player or NPC fields are serialized in `save_to_dict` / `load_from_dict`.
- [ ] **Location Suitability**: Romanceable NPCs define suitable private sectors in `metadata` table; public or hostile sectors block intimacy.
- [ ] **10-Step Narrative Arc & Unique Branching**: Major erotic encounters follow the full 10-step progression to climax and afterglow with appropriate mental purge rewards. Each foreplay branch has dedicated unique dialogue nodes from Step 4 through Step 10 Climax.
- [ ] **Step 1 Leave / Voluntary Retreat**: Erotic scenes provide an explicit option at Step 1 to decline or retreat back to safe hubs without triggering romance flags or rewards.
- [ ] **Deferred Intimacy Flags**: Step 1 choices set `is_intimacy_action: false`; `is_intimacy_action: true` is reserved exclusively for the Step 10 Climax transition.
- [ ] **Chapter Test Isolation**: Chapter-specific test suites reside under `tests/<chapter>/`, passing independently via `discover -s tests/<chapter>`.
