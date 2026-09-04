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

### The 5-Stage Narrative Progression
Structure major erotic sequences into distinct, descriptive narrative nodes:

1. **Stage 1: Tension & Unveiling / Disrobing (`<npc>_eroge_unveil`)**:
   - The private setting, palpable sexual tension, and removal of armor, robes, or clothing.
   - Vivid, sensory physical descriptions: exposed anatomy, curves, taut nipples, flushed skin, breathing, and scent.
2. **Stage 2: Sensual Foreplay & Oral Devotion (`<npc>_eroge_foreplay_*`)**:
   - Multiple branching choices (tender caresses, deep kisses, worship of intimate anatomy, uninhibited oral devotion).
   - Detailed vocal reactions: wanton gasps, whispered desires, trembling thighs, and mounting lubrication.
3. **Stage 3: Deep Penetrative Coupling (`<npc>_eroge_coupling` / `<npc>_companion_coupling`)**:
   - Deliberate, explicit description of penetration: snug fit, fevered heat, wet friction, and driving rhythm.
   - Dynamic posture choices (sensual missionary, intense from behind, or companion-led dominance).
   - Visceral sensory vocabulary: wet rhythmic slaps, stifled moans, clinging touches, and escalating momentum.
4. **Stage 4: Explosive Climax (`<npc>_eroge_climax` / `<npc>_companion_climax`)**:
   - Mutual, overwhelming orgasmic release: internal flooding, violent contractions, vocal release, and total surrender.
   - **Tangible Gameplay Rewards**:
     - Complete purge of negative mental states (Dread, Stress, or Insanity reset to 0).
     - Full devotion / relationship set to maximum (100).
     - Character marked as `is_romanced = True`.
     - Awarding unique permanent relics, accessories, or romantic perks.
5. **Stage 5: Tender Afterglow & Bonding (`<npc>_eroge_afterglow` / `<npc>_companion_afterglow`)**:
   - Quiet, lingering embrace, shared warmth, and emotional pillow talk.
   - Narrative transition to permanent romance, party recruitment opportunities, or unique future dialogue options.

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
In the party roster UI, each active companion card should offer direct interactive controls:
- **`[Talk]`**: Opens their dedicated companion dialogue hub.
- **`[♥ Intimate Scene]` / `[♥ Erotic Scene]`**: Rendered for romanceable female companions (`gender == 'female'` and `can_romance`). Initiates their explicit intimate scene directly from camp or travel.
- **`[Dismiss]`**: Respectfully sends the companion back to their home district or sanctuary.

### Dedicated Companion Dialogue Hubs (`<npc>_companion_hub`)
When speaking to an active party member, route them to a dedicated companion hub rather than their initial quest greeting:
- **Lore & Dialogue**: Discussions regarding their history, motivations, current events, and loyalty.
- **Traveler Intimacy**: Direct option to initiate secluded romantic encounters during travels.
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

# Multi-Stage Erotic Node (Climax Example)
DialogueNode(
    id="lyra_companion_climax",
    title="Lyra Valen - Mutual Surrender",
    narrative=(
        "Her gasps quicken into ragged, wanton cries as you drive into her warmth one final, unyielding time. "
        "Her inner walls flutter in violent spasms around you, clutching with desperate heat. With a shuddering groan, "
        "you spill yourself deep inside her, flooding her core as she arches back in total, breathless ecstasy."
    ),
    choices=[
        DialogueChoice(
            id="c_lyra_c_afterglow",
            text="Hold her close against your chest in the lingering warmth.",
            next_node="lyra_companion_afterglow",
            relationship_change=25
        )
    ]
)
```

### 3. Naming Conventions for Automated Routing
Maintain predictable ID suffixes so engine helper methods can resolve nodes dynamically:
- Companion Hub: `<npc_id>_companion_hub`
- Companion Intimacy Entry: `<npc_id>_companion_intimacy_start` or `<npc_id>_intimacy_scene`
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
- [ ] **Intimacy Scene Flow**: Multi-stage narrative erotic scenes progress smoothly from disrobing to climax without mini-game interruptions, purge negative mental stats, and award romance state.
- [ ] **Romance Constraints**: Ensure male companions follow the warrior brotherhood dynamic (`can_romance = False`) and minors/dependents are strictly non-combatant/non-romanceable.
- [ ] **Stat Checks**: Validate that difficulty targets properly account for player base stats, equipped items, and companion bonuses.
- [ ] **Hostility & Ambush**: Verify that NPCs with <= -50 relationship trigger immediate combat ambushes upon entering their sector.
- [ ] **Inventory & Economy**: Ensure items granted or purchased properly update player inventory, deduct currency, and trigger quest progression hooks.
