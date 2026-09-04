---
name: trpg-development
description: >-
  Develop, maintain, test, and expand adult eroge text RPG web applications.
  Use when authoring story chapters, designing NPCs and attribute systems,
  configuring JSON chapter content, heterosexual eroge romance, writing lengthy explicit narrative erotic scenes
  (without redundant minigames), implementing party companion interactions (dialogue hubs and intimacy initiation),
  party recruitment constraints, max party capacity, save/load/continue persistence, functional items,
  hostility mechanics, factions, and testing modular Flask and engine components.
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
  - **Modular JSON Content Architecture** (`game/data/<chapter>/`): All chapter-specific content (locations, factions, quests, NPCs, dialogues, metadata) is strictly separated into clean, modular JSON files rather than monolithic Python scripts. Python loader modules (`game/data/<chapter>.py`) deserialize these JSON files into typed dataclass instances.
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

## 2. Chapter Data Architecture (JSON Separation)

Avoid storing thousands of lines of narrative, dialogue, and location configurations in Python scripts. Separate all chapter content into structured JSON files under `game/data/<chapter_id>/`:

```
game/data/<chapter_id>/
├── metadata.json           # Chapter ID, title, opening chronicle log, suitable intimacy locations
├── factions.json           # Faction definitions (names, descriptions, UI theme colors)
├── locations.json          # Zones, descriptions, connections, ground inspection loot
├── quests.json             # Quest definitions, stages, and completion targets
├── npcs.json               # NPC stats, faction alignments, combatant/romance/recruitment flags
├── items.json              # Configurable quest items, progression keys, and romance relics
└── dialogues/              # Fully decoupled dialogue trees
    ├── <npc_1>.json
    ├── <npc_2>.json
    └── ...
```

### 1. `metadata.json`
```json
{
  "chapter_id": "prologue",
  "title": "The Iron Bell",
  "opening_log": "The great bell of the Bastion groans...",
  "suitable_intimacy_locations": {
    "sister_vanya": ["ruined_chantry", "gilded_rat"],
    "madame_silve": ["gilded_rat", "ruined_chantry"]
  }
}
```

### 2. `npcs.json` and Recruitment Flags
```json
{
  "sister_vanya": {
    "id": "sister_vanya",
    "name": "Sister Vanya",
    "title": "Acolyte of the Pale Veil",
    "gender": "female",
    "faction_id": "dawnshroud",
    "description": "Her habits are frayed, but her gaze is serene.",
    "stats": {"sinew": 8, "guile": 11, "lucidity": 15},
    "max_hp": 30,
    "current_hp": 30,
    "relationship": 0,
    "is_combatant": true,
    "can_romance": true,
    "can_recruit": true,
    "dialogue_root": "vanya_root",
    "loot": ["Sister Vanya's Embroidered Rosary"]
  },
  "commander_malakor": {
    "id": "commander_malakor",
    "name": "Commander Malakor",
    "title": "Captain of the Iron Drakes",
    "gender": "male",
    "faction_id": "iron_drakes",
    "description": "Clad in battered iron plate.",
    "stats": {"sinew": 16, "guile": 10, "lucidity": 9},
    "max_hp": 55,
    "current_hp": 55,
    "relationship": 0,
    "is_combatant": true,
    "can_romance": false,
    "can_recruit": false,
    "dialogue_root": "malakor_root",
    "loot": ["Malakor's Drake Whetstone"]
  }
}
```

### 3. `items.json` and Configurable Item Models
```json
{
  "wolfsbane_nectar": {
    "id": "wolfsbane_nectar",
    "name": "Wolfsbane Nectar",
    "description": "A sealed glass vial containing a potent narcotic extract distilled from purple mountain flowers.",
    "item_type": "quest",
    "is_usable": false,
    "effect_type": null,
    "effect_value": 0,
    "effect_description": ""
  },
  "vanya_rosary": {
    "id": "vanya_rosary",
    "name": "Sister Vanya's Embroidered Rosary",
    "description": "A silver rosary stitched with sacred prayer threads (+2 Lucidity, halves Dread gain; pray to purge 20 Dread).",
    "item_type": "quest",
    "is_usable": true,
    "effect_type": "dread_relief",
    "effect_value": 20,
    "effect_description": "Holding the silver rosary in your palms, memories of her passionate warmth flood your mind, driving away the dread."
  }
}
```

### 4. Chapter Loader Pattern (`game/data/<chapter>.py`)
Python chapter modules serve as typed loaders:
```python
import json
from pathlib import Path
from game.models import Location, NPC, Quest, DialogueNode, DialogueChoice, Item

DATA_DIR = Path(__file__).resolve().parent / "prologue"

def get_prologue_items() -> dict[str, Item]:
    with open(DATA_DIR / "items.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    items = {}
    for item_id, item_data in data.items():
        item = Item.from_dict(item_data)
        items[item_id] = item
        items[item.name] = item
    return items

def get_prologue_npcs():
    with open(DATA_DIR / "npcs.json", "r", encoding="utf-8-sig") as f:
        npcs_data = json.load(f)
    npcs = {}
    for npc_id, data in npcs_data.items():
        dialogue_file = DATA_DIR / "dialogues" / f"{npc_id}.json"
        dialogue_nodes = {}
        if dialogue_file.exists():
            with open(dialogue_file, "r", encoding="utf-8-sig") as df:
                d_data = json.load(df)
                for nid, n_dict in d_data.items():
                    dialogue_nodes[nid] = DialogueNode.from_dict(n_dict)
        data["dialogue_nodes"] = dialogue_nodes
        npcs[npc_id] = NPC.from_dict(data)
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

### The 10-Step Narrative Progression
Structure major erotic sequences into a continuous, richly descriptive 10-node progression:

1. **Step 1: Initiating (Seclusion & Disrobing)** (`<npc>_<loc>_step1_initiate` / `<npc>_intimacy_scene`):
   - Private retreat, atmospheric immersion, emotional vulnerability, and shedding armor/garments.
2. **Step 2: Sensual Foreplay & Branching Choices** (`<npc>_<loc>_step2_foreplay`):
   - At least 3 distinct narrative choices (e.g., Tender Romance, Dominant Passion, Devoted Oral / Sensory Indulgence).
3. **Step 3: Deepening Foreplay & Sensory Reaction** (`<npc>_<loc>_step3_<branch>`):
   - Visceral physical and vocal reactions to the chosen branch (flushed skin, wanton gasps, trembling thighs, lubrication).
4. **Step 4: Intimate Caresses & Lubrication** (`<npc>_<loc>_step4_caress`):
   - Tactile exploration, parting thighs, and spreading natural lubrication in anticipation of entry.
5. **Step 5: Penetration & Alignment** (`<npc>_<loc>_step5_entry`):
   - Deliberate, explicit description of penetration: alignment, stretching snug walls, taking full length to the root.
6. **Step 6: Initial Cadence & Deep Friction** (`<npc>_<loc>_step6_rhythm`):
   - Finding the rhythm, internal friction, suction, and breathless shared gasps.
7. **Step 7: Positional Shift & Escalation** (`<npc>_<loc>_step7_shift`):
   - Altering posture, angles, or elevation to target sensitive nerve centers with wet rhythmic impacts.
8. **Step 8: Fierce Cadence & Vocal Surrender** (`<npc>_<loc>_step8_frenzy`):
   - Relentless strokes, sweat-sheened skin, and uninhibited wanton cries drowning out external noise.
9. **Step 9: The Precipice (Edging / Pre-Climax)** (`<npc>_<loc>_step9_precipice`):
   - Involuntary passage spasms, desperate clutching, frantic breathing, and mutual surrender on the brink.
10. **Step 10: Explosive Climax** (`<npc>_<loc>_step10_climax`):
    - Mutual, overwhelming orgasmic release: internal flooding, violent contractions, vocal release, and total surrender.
    - **Tangible Gameplay Rewards**:
      - Complete purge of negative mental states (Dread, Stress, or Insanity reset to 0).
      - Full devotion / relationship set to maximum (100).
      - Character marked as `is_romanced = True`.
      - Awarding unique permanent relics, accessories, or romantic perks.

- **Afterglow & Bonding** (`<npc>_<loc>_afterglow`):
  - Quiet, lingering embrace, shared warmth, and emotional pillow talk.
  - Smooth narrative transition back to companion traveling hub (`<npc>_companion_hub`) or party recruitment (`<npc>_recruited`).

### Location Suitability Gating & Location-Unique Scenes
Intimacy requires seclusion, privacy, and atmospheric comfort. Companions will not engage in carnal intimacy in exposed, public, or hostile zones (e.g., gibbet squares, crowded mercenary yards, toxic sewer trenches):
1. **Suitability Mapping (`SUITABLE_INTIMACY_LOCATIONS`)**:
   - Maintain a dictionary mapping each romanceable NPC to their allowed sector IDs:
     ```python
     SUITABLE_INTIMACY_LOCATIONS = {
         "sister_vanya": ["ruined_chantry", "gilded_rat"],
         "madame_silve": ["gilded_rat", "ruined_chantry"]
     }
     ```
2. **Starting Location as Default Scene**:
   - The character's home district hosts their default erotic sequence (e.g., Sister Vanya in the sanctified crypt of the Ruined Chantry; Madame Silve in her velvet boudoir at the Gilded Rat).
3. **Location-Unique Intimate Narratives**:
   - Traveling to other suitable havens unlocks completely distinct 10-step erotic scenes reflecting environmental contrast (e.g., pious nun yielding to luxury on opium-scented crimson silks; worldly courtesan experiencing sacrilegious altar passion in a moonlit sanctuary).
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
└── <chapter_id>/                        # Chapter-Scoped Tests (e.g. tests/prologue/)
    ├── __init__.py
    ├── test_data_integrity.py           # Chapter: JSON schema validation & dialogue tree graph integrity
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

- [ ] **JSON Separation**: Story, dialogue trees, NPC profiles, locations, quests, and items reside in `game/data/<chapter>/` as JSON files, not hardcoded Python dicts.
- [ ] **Items Configuration & Anti-Bloat**: Items are defined in `items.json` using `Item` dataclasses. Filler consumable bloat is eliminated in favor of quest items, escape keys, and romance/brotherhood relics.
- [ ] **Dialogue Integrity**: Dialogue graphs validated: every `next_node` and `failure_node` targets an existing node with no broken links.
- [ ] **Recruitment Constraints**: Non-recruitable characters have `can_recruit: false`, have no party invitation choices in dialogues, and cannot be recruited via API.
- [ ] **Party Cap**: Max party size of 4 is respected across engine, API, and UI.
- [ ] **Save / Load Integrity**: All newly introduced player or NPC fields are serialized in `save_to_dict` / `load_from_dict`.
- [ ] **Location Suitability**: Romanceable NPCs define suitable private sectors in `metadata.json`; public or hostile sectors block intimacy.
- [ ] **10-Step Narrative Arc**: Major erotic encounters follow the full 10-step progression to climax and afterglow with appropriate mental purge rewards.
- [ ] **Chapter Test Isolation**: Chapter-specific test suites reside under `tests/<chapter>/`, passing independently via `discover -s tests/<chapter>`.
