---
name: trpg-development
description: >-
  Develop, maintain, test, and expand adult eroge text RPG web applications.
  Use when authoring story chapters, designing NPCs and attribute systems,
  configuring heterosexual eroge romance, writing lengthy explicit narrative erotic scenes
  (without redundant minigames), implementing party companion interactions (dialogue hubs and intimacy initiation),
  functional items, party recruitment, hostility mechanics, factions, and testing Flask backend endpoints.
---

# Adult Eroge Text RPG Development Skill

This skill provides comprehensive conventions, architectural patterns, narrative guidelines, and testing procedures for authoring and expanding **Adult Eroge Text RPG** web applications.

---

## 1. Architectural Patterns & Technical Foundation

### Core Stack
- **Backend**: Python with Flask (or similar lightweight framework) providing a stateless or session-driven REST API (`/api/state`, `/api/action`).
- **Engine Core**: Pure Python domain layer decoupled from HTTP concerns.
  - `models.py`: Dataclasses for Player, Stats, NPC, Quest, Faction, Location, DialogueNode, DialogueChoice, Item.
  - `engine.py`: Central state machine handling location traversal, dynamic dialogue resolution, attribute checks with gear/companion buffs, multi-stage explicit erotic encounters, party recruitment, companion dialogue hubs, faction hostility, inventory management, and tactical turn-based combat.
  - Content Modules (`game/data/*.py`): Modular data definitions containing sector descriptions, NPC profiles, dialogue trees, items, and quest stages.
- **Frontend**: Lightweight, reactive single-page client (HTML5, CSS3, vanilla JavaScript).
  - Narrative chronicle displaying environmental prose and event history.
  - Interactive dialogue choice overlays.
  - Vitals, stats, and status meters (Health, Morale/Dread, Stamina, Currency).
  - Interactive inventory / haversack.
  - Companion / Warband roster with dedicated quick-action controls.
- **Testing**:
  - Test suite (`unittest` / `pytest`) verifying state transitions, dialogue routing, attribute check calculations, quest lifecycles, and companion intimacy flows.

---

## 2. Narrative & Eroge Design Principles

### Balance of Gameplay and Intimacy
A high-quality eroge text RPG maintains approximately a **50% gameplay / 50% erotic romance** balance:
- The game is a fully realized RPG with tactical survival, exploration, questing, and consequences.
- Erotic encounters are meaningful narrative milestones and emotional payoffs, not hollow isolated minigames.

### Heterosexual Romance & Companion Archetypes
1. **Adult Male Protagonist**: The narrative perspective centers on an adult male protagonist.
2. **Consenting Adult Female Romanceable Characters (`can_romance: True`)**:
   - Romance and erotic encounters are strictly heterosexual and involve consenting adult female characters.
   - Built on affection, shared hardship, emotional vulnerability, and mutual respect.
   - High relationship/devotion unlocks dedicated intimate scenes, companion abilities, and party loyalty.
3. **Male Companions & Comrades (`can_romance: False`)**:
   - Male companions feature a dedicated **Warrior Brotherhood & Camaraderie** dynamic.
   - Character arcs focus on battlefield trust, sparring, shared rations or drinks, oaths of loyalty, and tactical coordination.
4. **Protection of Innocents & Minors**:
   - Any non-combatant elders, dependents, or minor NPCs are strictly **non-romanceable** and non-combatants.
   - Interactions are strictly focused on mentorship, protection, rescue, and humanitarian relief.

---

## 3. Lengthy Explicit Narrative Erotic Scenes

### Elimination of Redundant Minigames
- Avoid mechanical intimacy mini-games (arousal bars, stamina friction gauges, rhythm QTEs, technique check loops). They disrupt narrative immersion, feel repetitive, and distract from prose quality.
- All intimate encounters must flow naturally through **rich, multi-stage narrative dialogue trees**.

### The 10-Step Narrative Progression
Structure major erotic sequences into a continuous, richly descriptive 10-node progression:

1. **Step 1: Initiating (Seclusion & Disrobing)** (`<npc>_<loc>_step1_initiate` / `<npc>_intimacy_scene`):
   - Private retreat, environmental atmosphere, emotional vulnerability, and shedding armor/robes down to intimate undergarments.
2. **Step 2: Sensual Foreplay & Branching Choices** (`<npc>_<loc>_step2_foreplay`):
   - At least 3 distinct narrative choices (e.g., Tender Romance, Dominant Passion, Devoted Oral / Sensory Indulgence).
3. **Step 3: Deepening Foreplay & Sensory Reaction** (`<npc>_<loc>_step3_<branch>`):
   - Visceral physical and vocal reactions to the chosen foreplay branch (flushed skin, wanton gasps, trembling thighs, and rising lubrication).
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
   - The character's home district or sanctuary hosts their default erotic sequence (e.g., Sister Vanya in the sanctified crypt of the Ruined Chantry; Madame Silve in her velvet boudoir at the Gilded Rat).
3. **Location-Unique Intimate Narratives**:
   - Traveling to other suitable havens unlocks completely distinct 10-step erotic scenes reflecting the contrast of the environment (e.g., pious nun yielding to sinful luxury on opium-scented crimson silks; worldly courtesan experiencing sacrilegious altar passion in a moonlit sanctuary).
4. **Companion Dialogue Hub Gating**:
   - In `<npc>_companion_hub`, choices with `is_intimacy_action = True` are filtered out dynamically unless `can_initiate_companion_erotic(npc_id)` evaluates to `True`.
5. **Direct Erotic Scene Dispatch**:
   - `start_party_erotic_scene(npc_id)` checks `can_initiate_companion_erotic(npc_id)`. If in an unsuitable sector, it returns an immersive in-world error guiding the player to seek a secluded haven. When in a suitable sector, it routes dynamically via `get_companion_erotic_node_id(npc)`.

### Prose & Tone Guidelines
- Use explicit, mature anatomical vocabulary without resorting to sterile clinical terms or comical euphemisms.
- Focus equally on **physical sensations** (heat, moisture, tightness, friction), **auditory details** (breathing, stifled cries, wet sounds), and **emotional connection** (desire, vulnerability, devotion).

---

## 4. Party Recruitment & Companion Systems

### Recruitment Mechanics
- Viable combatants (`is_combatant: True`) with high disposition (e.g., `relationship >= 50`) can be recruited into the active party (typically capped at 2–3 companions).
- Recruited companions provide mechanical bonuses:
  - **Attribute Buffs**: Adding a fraction (e.g., +1/4 or +1/3) of companion attributes to player effective checks.
  - **Combat Assistance**: Extra damage, secondary strikes, or defensive cover in encounters.

### Companion UI Action Controls
In the party roster UI, each active companion card offers direct interactive controls:
- **`[Talk]`**: Opens their dedicated companion dialogue hub (`<npc>_companion_hub`).
- **`[♥ Erotic Scene]`**: Rendered exclusively for romanceable female companions (`gender == 'female'`, `can_romance: True`) when **`c.can_initiate_erotic` is True** (i.e. party is currently in a suitable location). Initiates their location-unique explicit intimate scene directly.
- **`[Dismiss]`**: Respectfully sends the companion back to their home district or sanctuary.

### Dedicated Companion Dialogue Hubs (`<npc>_companion_hub`)
When speaking to an active party member, route them to a dedicated companion hub rather than their initial quest greeting:
- **Lore & Dialogue**: Discussions regarding their history, motivations, current events, and loyalty.
- **Traveler Intimacy**: Direct option to initiate secluded romantic encounters during travels (only visible when in a suitable location).
- **Special Companion Support Abilities**:
  - Medical / Triage healing (restores Health, reduces Stress/Dread).
  - Supplies & Logistics (gifting rations, wine, lockpicks, or currency).
  - Combat Tactics / Sparring (buffs, stamina recovery, tactical advice).
  - Camp Rest / Sharing drinks (soothes negative mental states).
- **Dismissal**: Polite farewell choice that unbinds them from the party.

---

## 5. Attribute Systems & Dialogue Checks

### Custom Attribute Triads
Avoid generic RPG tropes when possible. Tailor attribute systems to the theme of the game:
- **Physical Force / Resilience**: (e.g., *Sinew*, *Might*, *Vigor*) — Used for raw force, heavy blows, intimidation, endurance, and physical stamina.
- **Agility / Precision**: (e.g., *Guile*, *Finesse*, *Cunning*) — Used for reflexes, stealth, lockpicking, precision strikes, and delicate erogenous touch.
- **Mental / Occult Fortitude**: (e.g., *Lucidity*, *Focus*, *Willpower*) — Used for perception, detecting lies, resisting horror/dread, occult insights, and emotional resonance.

### Dialogue Check Resolution
Attribute checks compare the player's **effective attribute** against a difficulty target:
$$\text{Effective Stat} = \text{Base Stat} + \sum \text{Gear Bonuses} + \sum \text{Companion Bonuses}$$
- Successful checks grant rewards, advance quests without violence, or deepen romantic intimacy.
- Failed checks should lead to interesting complications (alarm raised, combat initiated, temporary relationship loss) rather than dead ends.

---

## 6. Dynamic Dialogue Routing Conventions

When an NPC interaction begins via `engine.talk_npc(npc_id)`, route dialogue according to the following strict priority order:

1. **Hostility / Attack-on-Sight Ambush**:
   - If `npc.relationship <= -50` (or hostile faction state), abort conversation immediately and trigger lethal combat (`ambush=True`).
2. **In-Party Companion Hub (`<npc>_companion_hub`)**:
   - If the NPC is currently an active party member, route directly to `get_companion_hub_id(npc)`.
3. **Quest Turn-In Node (`<npc>_quest_complete`)**:
   - If the player possesses the quest's required item, transition directly to turn-in and reward dialogues.
4. **Completed Quest Aftermath Node**:
   - If the NPC's quest is completed (`stage == 99`), load their post-quest dialogue state rather than resetting to initial greetings.
5. **Active Quest Reminder Node (`<npc>_quest_accepted`)**:
   - If the quest is in progress but items are missing, display reminder dialogues rather than re-triggering intro dialogues.
6. **State-Based Resolution**:
   - For transient or rescued NPCs, maintain persistent aftermath states (e.g., saved vs. extorted).
7. **Default Greeting Node**:
   - Fall back to `npc.dialogue_root` (typically `"root"`).

---

## 7. Adding & Extending Game Content

### 1. Defining an NPC
```python
NPC(
    id="lyra_valen",
    name="Lyra Valen",
    title="The Silver Scout",
    gender="female",
    faction_id="rebel_vanguard",
    description="A sharp-eyed scout clad in supple boiled leather.",
    stats=Stats(sinew=10, guile=16, lucidity=12),
    max_hp=32,
    current_hp=32,
    relationship=0,
    is_combatant=True,
    can_romance=True, # Consenting adult female companion
    dialogue_root="root",
    dialogue_nodes={...},
    loot=["Scout's Stiletto", "Supple Leather Jerkin"]
)
```

### 2. Defining Companion Hub & Intimate Scene Nodes
```python
# Companion Hub
DialogueNode(
    id="lyra_companion_hub",
    title="Lyra Valen - Scouting Camp",
    narrative="Lyra cleans her stiletto by the firelight. 'Need something scouted, or just looking to pass the watch together?'",
    choices=[
        DialogueChoice(
            id="c_lyra_talk",
            text="Talk about her past in the frontier.",
            next_node="lyra_companion_talk"
        ),
        DialogueChoice(
            id="c_lyra_intimacy",
            text="Draw her into the warmth of your tent. [Intimate Scene]",
            next_node="lyra_companion_intimacy_start"
        ),
        DialogueChoice(
            id="c_lyra_scout",
            text="Ask her to scout ahead for safe paths. (+Guile check buff)",
            next_node="lyra_companion_scout_buff"
        ),
        DialogueChoice(
            id="c_lyra_dismiss",
            text="Request that she return to the outpost. [Dismiss from Party]",
            next_node="lyra_companion_dismiss"
        )
    ]
)

# 10-Step Erotic Node Progression Example (Step 10 Climax & Afterglow)
DialogueNode(
    id="lyra_camp_step10_climax",
    speaker_name="Lyra Valen",
    text=(
        "Her gasps quicken into ragged, wanton cries as you drive into her warmth one final, unyielding time. "
        "Her inner walls flutter in violent spasms around you, clutching with desperate heat. With a shuddering groan, "
        "you spill yourself deep inside her, flooding her core as she arches back in total, breathless ecstasy."
    ),
    choices=[
        DialogueChoice(
            id="c_lyra_camp_to_afterglow",
            text="Hold her close against your chest in the lingering warmth.",
            next_node="lyra_camp_afterglow",
            is_intimacy_action=True,
            relationship_change=25,
            item_reward="Lyra's Silver Whistle"
        )
    ]
)

DialogueNode(
    id="lyra_camp_afterglow",
    speaker_name="Lyra Valen",
    text=(
        "Reclined in the warmth of the tent blankets, Lyra rests her flushed cheek upon your chest. "
        "'I never knew surviving could feel this sweet,' she whispers softly, placing her silver scout's whistle into your palm. "
        "'Whenever darkness closes in, wanderer, know that I am yours.'"
    ),
    choices=[
        DialogueChoice(
            id="c_lyra_camp_return_hub",
            text="Adjust your leather armor and return to traveling together.",
            next_node="lyra_companion_hub"
        )
    ]
)
```

### 3. Naming Conventions for Automated Routing
Maintain predictable ID suffixes so engine helper methods can resolve nodes dynamically:
- Companion Hub: `<npc_id>_companion_hub`
- Location-Specific 10-Step Starting Node: `<npc>_<loc>_step1_initiate`
- 10-Step Sequence Nodes:
  - Step 1: `<npc>_<loc>_step1_initiate`
  - Step 2: `<npc>_<loc>_step2_foreplay`
  - Step 3: `<npc>_<loc>_step3_<branch>` (e.g., `step3_tender`, `step3_dominant`, `step3_oral`)
  - Step 4: `<npc>_<loc>_step4_caress`
  - Step 5: `<npc>_<loc>_step5_entry`
  - Step 6: `<npc>_<loc>_step6_rhythm`
  - Step 7: `<npc>_<loc>_step7_shift`
  - Step 8: `<npc>_<loc>_step8_frenzy`
  - Step 9: `<npc>_<loc>_step9_precipice`
  - Step 10: `<npc>_<loc>_step10_climax`
  - Afterglow: `<npc>_<loc>_afterglow`
- Companion Intimacy Entry Fallback: `<npc_id>_companion_intimacy_start` or `<npc_id>_intimacy_scene`
- Quest Turn-in: `<npc_id>_quest_complete`
- Quest In-Progress: `<npc_id>_quest_accepted`

---

## 8. Verification & Quality Assurance Workflows

### 1. Test Suite Execution
Maintain comprehensive automated tests covering all critical mechanics:
```powershell
$env:PYTHONPATH = "."
& "D:\Anaconda\python.exe" -m unittest discover -s tests -p "test_*.py"
```

### 2. Testing Checklist for New Content
- [ ] **Dialogue Integrity**: Ensure all `next_node` and `fail_node` references point to existing nodes (no broken references or dead ends).
- [ ] **Companion Hub Integrity**: Recruited companions route directly to `<npc>_companion_hub` and can be dismissed and re-recruited.
- [ ] **10-Step Sequence Completeness**: Every erotic narrative path progresses uninterrupted through all 10 sequential stages (Initiating -> Foreplay Branch -> Deepening Foreplay -> Caress -> Entry -> Rhythm -> Shift -> Frenzy -> Precipice -> Climax -> Afterglow).
- [ ] **Location Suitability Gating**: Intimacy is strictly blocked in unsuitable sectors (`can_initiate_companion_erotic` returns `False`, party UI button hidden, hub choice hidden, direct action returns friendly error).
- [ ] **Location-Unique Content**: Verify that traveling to different suitable locations launches the appropriate unique 10-step sequence (starting location as default, secondary locations with custom atmospheric narrative).
- [ ] **Erotic Rewards & State**: Climax purges dread/stress to 0, sets relationship to maximum (100), flags `is_romanced = True`, and awards designated keepsake items.
- [ ] **Romance Constraints**: Ensure male companions follow the warrior brotherhood dynamic (`can_romance = False`) and minors/dependents are strictly non-combatant/non-romanceable.
- [ ] **Stat Checks**: Validate that difficulty targets properly account for player base stats, equipped items, and companion bonuses.
- [ ] **Hostility & Ambush**: Verify that NPCs with <= -50 relationship trigger immediate combat ambushes upon entering their sector.
- [ ] **Inventory & Economy**: Ensure items granted or purchased properly update player inventory, deduct currency, and trigger quest progression hooks.
