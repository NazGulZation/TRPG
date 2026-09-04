"""Prologue chapter data: 'Ashen Solstice - The Sinking of Oakhaven'."""

from typing import Dict
from game.models import Stats, NPC, Location, Quest, QuestStage, DialogueNode, DialogueChoice

SUITABLE_INTIMACY_LOCATIONS = {
    "sister_vanya": ["ruined_chantry", "gilded_rat"],
    "madame_silve": ["gilded_rat", "ruined_chantry"]
}

def get_prologue_locations() -> Dict[str, Location]:
    return {
        "gallow_square": Location(
            id="gallow_square",
            name="The Gallow-Square of Weeping Wood",
            subtitle="Ground Zero of the Quarantine",
            description=(
                "Thick, greasy soot clings to the timber gibbets where corpses of suspected plague-bearers sway in iron cages. "
                "The air tastes of sulfur, wet rot, and dried blood. High above, the iron portcullis of Oakhaven remains firmly shut, "
                "streaked with scorched tallow. A brass bell tolls intermittently from the watchtower—a death knell warning that "
                "the cleansing pyre will ignite at midnight."
            ),
            faction_id="pariahs",
            connected_locations=["ruined_chantry", "iron_bastion", "sluice_trench"],
            npc_ids=["little_toby"],
            items_on_ground=["Tarnished Iron Nail"],
            danger_level=1
        ),
        "ruined_chantry": Location(
            id="ruined_chantry",
            name="The Desecrated Chantry of Saint Marrow",
            subtitle="Makeshift Hospice and Dawnshroud Outpost",
            description=(
                "Stained glass lies shattered amidst kneeling skeletons. Alchemical braziers burn dried sage and pungent hemlock "
                "to mask the stench of liquefying lungs. White shrouds cover rows of the dying. Here, the Order of the Dawnshroud "
                "separates the 'purifiable' from the doomed with cold, clinical mercy."
            ),
            faction_id="dawnshroud",
            connected_locations=["gallow_square", "iron_bastion"],
            npc_ids=["sister_vanya"],
            items_on_ground=["Purified Bandage"],
            danger_level=2
        ),
        "iron_bastion": Location(
            id="iron_bastion",
            name="The Iron Drake Bastion & Pit",
            subtitle="Mercenary Redoubt and Black Market",
            description=(
                "A fortified brewery turned garrison. Piles of weapons, looted church silver, and kegs of harsh rye gin fill the courtyard. "
                "Mercenaries in dented mail wager on pit dogs while sharpening broadswords. The Drakes hold the barricades, charging desperate "
                "refugees exorbitant ransoms for false transit seals."
            ),
            faction_id="iron_drakes",
            connected_locations=["gallow_square", "ruined_chantry", "gilded_rat"],
            npc_ids=["commander_malakor"],
            items_on_ground=["Heavy Whetstone"],
            danger_level=3
        ),
        "gilded_rat": Location(
            id="gilded_rat",
            name="The Gilded Rat Parlour",
            subtitle="A Den of Carnal Solace and Smuggled Secrets",
            description=(
                "Heavy velvet drapes seal off the toxic smoke of the streets. Opium smoke curls in the candlelight, mingling with cheap perfume "
                "and sweat. Men and women seeking one final touch of warmth before the purge spend their last silver sovereigns here. "
                "In the curtained alcoves, forbidden information and forged transit passes trade hands."
            ),
            faction_id="pariahs",
            connected_locations=["iron_bastion", "sluice_trench"],
            npc_ids=["madame_silve"],
            items_on_ground=["Spiced Plum Wine"],
            danger_level=1
        ),
        "sluice_trench": Location(
            id="sluice_trench",
            name="The Smuggler's Sluice & Trench",
            subtitle="The Subterranean Drainage of the Condemned",
            description=(
                "Knee-deep in black bile and drainage run-off, the Trench smells of stagnant canal water and decay. "
                "It is the only unmonitored artery leading beyond Oakhaven's outer wall, but the iron grate is secured by a triple-toothed lock. "
                "Without the master key or brute demolition, this channel is an inescapable tomb."
            ),
            faction_id="pariahs",
            connected_locations=["gallow_square", "gilded_rat"],
            npc_ids=[],
            items_on_ground=["Corroded Crowbar"],
            danger_level=4
        )
    }

def get_prologue_npcs() -> Dict[str, NPC]:
    vanya_dialogues = {
        "root": DialogueNode(
            id="root",
            speaker_name="Sister Vanya",
            text=(
                "The sister looks up from a blood-soaked linen cot, pushing strands of sweat-matted dark hair from her fevered eyes. "
                "Her white habit is smeared with charcoal and arterial red, the coarse cloth clinging to her trembling frame. "
                "'Another wanderer,' she whispers, her voice husky and ragged with exhaustion. "
                "'Are you here seeking absolution, or are your veins already burning with the black-rot?'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_examine",
                    text="[Lucidity 11] 'Your hands tremble, Sister. You are administering hemlock, not medicine. You are mercy-killing them.'",
                    next_node="vanya_lucidity_success",
                    required_stat="lucidity",
                    required_value=11,
                    relationship_change=10,
                    failure_node="vanya_lucidity_fail"
                ),
                DialogueChoice(
                    id="c_vanya_triage",
                    text="[Lucidity 10] 'Let me help you examine the patients in this ward before the bell strikes.'",
                    next_node="vanya_triage_ward",
                    required_stat="lucidity",
                    required_value=10,
                    relationship_change=10
                ),
                DialogueChoice(
                    id="c_vanya_help",
                    text="'I am still breathing. Tell me how I can assist your work before the midnight purge.'",
                    next_node="vanya_quest_hook",
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_vanya_flirt",
                    text="Step closer, brushing the soot from her cheek. 'Even in this charnel house, your beauty is a cruel reminder of life.'",
                    next_node="vanya_romance_start",
                    is_romance_action=True,
                    relationship_change=10
                ),
                DialogueChoice(
                    id="c_vanya_insult",
                    text="'You Dawnshroud hypocrites are burning innocent people alive. You deserve the pyre as much as they do.'",
                    next_node="vanya_hostile",
                    relationship_change=-25,
                    faction_changes={"dawnshroud": -15},
                    is_hostile_action=True
                )
            ]
        ),
        "vanya_triage_ward": DialogueNode(
            id="vanya_triage_ward",
            speaker_name="Sister Vanya",
            text=(
                "Vanya's eyes widen with cautious gratitude as you step into the lantern glow. Three cots demand urgent triage: "
                "a convulsing Dawnbound soldier choking on blackened sputum, an infected youth with swollen lymphatic carbuncles, "
                "and an elderly woman weeping incoherently from delirium."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_triage_soldier",
                    text="[Sinew 12] Hold the seizing soldier down firmly while Vanya safely inserts a silver airway pipe.",
                    next_node="vanya_triage_soldier_success",
                    required_stat="sinew",
                    required_value=12,
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_vanya_triage_youth",
                    text="[Guile 11] Use your scalpel or dirk with surgical precision to drain the carbuncle cleanly.",
                    next_node="vanya_triage_youth_success",
                    required_stat="guile",
                    required_value=11,
                    relationship_change=15,
                    item_reward="Purified Bandage"
                ),
                DialogueChoice(
                    id="c_vanya_triage_return",
                    text="'We must focus on getting the medicine from Malakor.'",
                    next_node="vanya_quest_hook"
                )
            ]
        ),
        "vanya_triage_soldier_success": DialogueNode(
            id="vanya_triage_soldier_success",
            speaker_name="Sister Vanya",
            text=(
                "With muscular resilience, you pin the thrashing templar's shoulders to the cot. Vanya swiftly clears his throat of black bile. "
                "The soldier's breathing stabilizes into calm sleep. Vanya wipes a drop of sweat from her lip, looking up at you with flushed cheeks. "
                "'You have powerful hands, wanderer... and a gentle heart. Thank you.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_after_triage",
                    text="'Tell me what else we need to save these people.'",
                    next_node="vanya_quest_hook"
                )
            ]
        ),
        "vanya_triage_youth_success": DialogueNode(
            id="vanya_triage_youth_success",
            speaker_name="Sister Vanya",
            text=(
                "Your steady hands lance the lethal pocket with microscopic care. The feverish boy sighs in relief as the poisonous pressure abates. "
                "Vanya wraps him in clean dressings, pressing a spare Purified Bandage into your palm. "
                "'Extraordinary dexterity. You would have made a brilliant surgeon in the capital.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_after_triage2",
                    text="'Now tell me where the hemlock is.'",
                    next_node="vanya_quest_hook"
                )
            ]
        ),
        "vanya_lucidity_success": DialogueNode(
            id="vanya_lucidity_success",
            speaker_name="Sister Vanya",
            text=(
                "Vanya stiffens, her gaze darting to the armed Dawnbound zealots outside. A ragged breath leaves her trembling lips. "
                "'Quiet, fool!' she hisses, stepping so close you can feel the heat of her breath. 'The Inquisitor demands they burn alive to purge their sins. "
                "I... I cannot watch another child scream in the phosphorus cages. I grant them painless sleep. But my vial of Wolfsbane Nectar is dry. "
                "Without it, the remaining eight in this ward will burn screaming at midnight.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_accept_quest",
                    text="'I will find your Wolfsbane Nectar. Where can it be procured?'",
                    next_node="vanya_quest_details",
                    relationship_change=15,
                    quest_trigger="q_mercy_hemlock",
                    quest_stage_set=1
                ),
                DialogueChoice(
                    id="c_vanya_comfort",
                    text="Gently grasp her hand. 'You are carrying a terrible burden alone. Let me bear some of it with you.'",
                    next_node="vanya_tender_moment",
                    relationship_change=15,
                    is_romance_action=True
                )
            ]
        ),
        "vanya_lucidity_fail": DialogueNode(
            id="vanya_lucidity_fail",
            speaker_name="Sister Vanya",
            text=(
                "She pulls back defensively, hiding the dark apothecary vial beneath her cowl. "
                "'Do not feign understanding of the Sacred Rites, stranger. If you have nothing useful to offer, leave my chantry.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_back_to_root",
                    text="'Forgive me. How can I help?'",
                    next_node="vanya_quest_hook"
                )
            ]
        ),
        "vanya_quest_hook": DialogueNode(
            id="vanya_quest_hook",
            speaker_name="Sister Vanya",
            text=(
                "'The Iron Drakes looted the chantry apothecary hours ago. Commander Malakor holds the only remaining supply of Wolfsbane Nectar "
                "in his garrison. He considers it poison to sell to assassins. If you bring it back to me, I can spare these souls from agony, "
                "and I will give you the Dawnshroud Sanctified Seal to pass the outer guard.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_accept_quest_direct",
                    text="'Consider it done. I will retrieve the Wolfsbane Nectar.'",
                    next_node="vanya_quest_accepted",
                    relationship_change=10,
                    quest_trigger="q_mercy_hemlock",
                    quest_stage_set=1
                )
            ]
        ),
        "vanya_quest_details": DialogueNode(
            id="vanya_quest_details",
            speaker_name="Sister Vanya",
            text=(
                "'Malakor is entrenched at the old brewery bastion. He is brutal, but respects strength or coin. Do whatever it takes to bring the nectar back.'"
            ),
            choices=[]
        ),
        "vanya_quest_accepted": DialogueNode(
            id="vanya_quest_accepted",
            speaker_name="Sister Vanya",
            text=(
                "'May the Silent Martyrs shield your steps. Malakor is ruthless—do not let him gut you before you negotiate or pry it from his grip.'"
            ),
            choices=[]
        ),
        "vanya_quest_complete": DialogueNode(
            id="vanya_quest_complete",
            speaker_name="Sister Vanya",
            text=(
                "Tears carve pale trails through the ash on Vanya's cheeks as she takes the dark vial from your hands. "
                "'You... you truly brought it. They will slip away into darkness without feeling the flames.' She presses a silver Dawnshroud Seal "
                "into your palm, her fingers lingering against your skin, warm and trembling. Her eyes carry a deep, burning hunger for solace."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_embrace",
                    text="Pull her into your arms amidst the shadowed arches of the ruined chantry.",
                    next_node="vanya_intimacy_scene",
                    is_intimacy_action=True,
                    relationship_change=25
                ),
                DialogueChoice(
                    id="c_vanya_ask_party",
                    text="'The chantry is doomed, Vanya. Come with me. Join my party and let us break through the perimeter together.'",
                    next_node="vanya_recruited",
                    relationship_change=15
                )
            ]
        ),
        "vanya_romance_start": DialogueNode(
            id="vanya_romance_start",
            speaker_name="Sister Vanya",
            text=(
                "Vanya shivers at your touch. Her skin is feverishly warm beneath the soot. For a moment, her religious composure fractures completely, "
                "revealing a lonely, terrified woman starved of tenderness and carnal warmth. 'You are reckless to speak like that in a city awaiting the torch,' "
                "she whispers, though she leans into your palm, her lips parting as she exhales a soft, ragged breath."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_romance_push",
                    text="'When death is hours away, truth is all that matters. Help me, and let me keep you alive tonight.'",
                    next_node="vanya_quest_hook",
                    relationship_change=15,
                    is_romance_action=True
                )
            ]
        ),
        "vanya_tender_moment": DialogueNode(
            id="vanya_tender_moment",
            speaker_name="Sister Vanya",
            text=(
                "She clutches your hand tightly, her nails biting into your callused palm. 'I thought everyone left in Oakhaven was either a butcher "
                "or a corpse. If you retrieve that wolfsbane from Malakor, I swear by my own blood that I will not leave your side.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_accept_after_tender",
                    text="'Wait for me here. I will return with it.'",
                    next_node="vanya_quest_accepted",
                    quest_trigger="q_mercy_hemlock",
                    quest_stage_set=1
                )
            ]
        ),

        # --- Sister Vanya 10-Step Erotic Sequence: The Desecrated Chantry (Default Scene) ---
        # Step 1: Initiating (Seclusion & Disrobing)
        "vanya_intimacy_scene": DialogueNode(
            id="vanya_intimacy_scene",
            speaker_name="Sister Vanya",
            text=(
                "Leading you behind the heavy tattered velvet altar curtain into the consecrated crypt, Vanya shuts out the toxic smog of Oakhaven. "
                "A solitary wax taper flickers upon an alabaster pedestal, casting golden warmth across her flushed skin. "
                "Her dark hair spills loose over her shoulders as she unpins her wimple. "
                "'All my life I was taught that the flesh is a vessel of sin,' she whispers, her breath trembling against your collarbone. "
                "'Yet tonight, with the fire hours away... all I want is to feel your heat, wanderer. Show me what life feels like before we burn.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step2",
                    text="Reach for the lacings of her habit, gently stripping away her sacred vows.",
                    next_node="vanya_chantry_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_vanya_eroge_unveil",
                    text="Reach for the lacings of her habit, gently stripping away her sacred vows.",
                    next_node="vanya_chantry_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        "vanya_chantry_step1_initiate": DialogueNode(
            id="vanya_chantry_step1_initiate",
            speaker_name="Sister Vanya",
            text=(
                "Leading you behind the heavy tattered velvet altar curtain into the consecrated crypt, Vanya shuts out the toxic smog of Oakhaven. "
                "A solitary wax taper flickers upon an alabaster pedestal, casting golden warmth across her flushed skin. "
                "Her dark hair spills loose over her shoulders as she unpins her wimple. "
                "'All my life I was taught that the flesh is a vessel of sin,' she whispers, her breath trembling against your collarbone. "
                "'Yet tonight, with the fire hours away... all I want is to feel your heat, wanderer. Show me what life feels like before we burn.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_step1_choice",
                    text="Reach for the lacings of her habit, gently stripping away her sacred vows.",
                    next_node="vanya_chantry_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        # Step 2: Foreplay & Branching Choices
        "vanya_chantry_step2_foreplay": DialogueNode(
            id="vanya_chantry_step2_foreplay",
            speaker_name="Sister Vanya",
            text=(
                "With patient, deliberate care, your fingers untie the stained cord of her habit. The heavy white cloth slips to the stone, "
                "leaving her dressed only in a sheer linen chemise damp with perspiration. Beneath the translucent fabric, her full, rose-tipped breasts "
                "heave with every breath, her taut nipples pressing visibly against the cloth. "
                "She shivers not from cold, but from sheer sensory overload as your hands cup her waist. Her lips part with a shuddering gasp, "
                "inviting you deeper into her sanctuary."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_branch_tender",
                    text="[Tender Romance] Gently push the chemise off her shoulders and kiss down her throat to her breasts.",
                    next_node="vanya_chantry_step3_tender",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_chantry_branch_dominant",
                    text="[Dominant Passion] Lift her bodily onto the stone altar, parting her bare thighs before you.",
                    next_node="vanya_chantry_step3_dominant",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_chantry_branch_oral",
                    text="[Devoted Worship] Kneel between her trembling thighs and lavish her glistening core with oral devotion.",
                    next_node="vanya_chantry_step3_oral",
                    is_intimacy_action=True
                ),
                # Aliases for backward compatibility
                DialogueChoice(
                    id="c_vanya_eroge_tender",
                    text="Gently push the chemise off her shoulders and kiss down her throat to her breasts.",
                    next_node="vanya_chantry_step3_tender",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_dominant",
                    text="Lift her bodily onto the stone altar, parting her bare thighs before you.",
                    next_node="vanya_chantry_step3_dominant",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_oral",
                    text="Kneel between her trembling thighs and lavish her glistening core with devoted oral worship.",
                    next_node="vanya_chantry_step3_oral",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_unveil": DialogueNode(
            id="vanya_eroge_unveil",
            speaker_name="Sister Vanya",
            text=(
                "With patient, deliberate care, your fingers untie the stained cord of her habit. The heavy white cloth slips to the stone, "
                "leaving her dressed only in a sheer linen chemise damp with perspiration. Beneath the translucent fabric, her full, rose-tipped breasts "
                "heave with every breath, her taut nipples pressing visibly against the cloth. "
                "She shivers not from cold, but from sheer sensory overload as your hands cup her waist. Her lips part with a shuddering gasp, "
                "inviting you deeper into her sanctuary."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_tender_alias",
                    text="Gently push the chemise off her shoulders and kiss down her throat to her breasts.",
                    next_node="vanya_chantry_step3_tender",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_dominant_alias",
                    text="Lift her bodily onto the stone altar, parting her bare thighs before you.",
                    next_node="vanya_chantry_step3_dominant",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_oral_alias",
                    text="Kneel between her trembling thighs and lavish her glistening core with devoted oral worship.",
                    next_node="vanya_chantry_step3_oral",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 3: Deepening Foreplay (Branch Outcomes)
        "vanya_chantry_step3_tender": DialogueNode(
            id="vanya_chantry_step3_tender",
            speaker_name="Sister Vanya",
            text=(
                "Your mouth traces the delicate curve of her collarbone down to the soft swell of her breast. When your lips capture her erect nipple, "
                "suckling with gentle heat, Vanya lets out an arched, quivering cry, her nails digging into your back. "
                "Your hand slides down her silken belly into the humid heat between her thighs, finding her already slick and drenched with longing. "
                "She whimpers, grinding her hips into your palm with uninhibited hunger. 'Wanderer... please... I feel as though my entire soul is catching fire...'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_tender_to_step4",
                    text="Slide your fingers into her drenched warmth, stroking her with deliberate passion.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_enter_tender",
                    text="Align your hips with hers and push smoothly into her velvet warmth.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_foreplay_tender": DialogueNode(
            id="vanya_eroge_foreplay_tender",
            speaker_name="Sister Vanya",
            text=(
                "Your mouth traces the delicate curve of her collarbone down to the soft swell of her breast. When your lips capture her erect nipple, "
                "suckling with gentle heat, Vanya lets out an arched, quivering cry, her nails digging into your back. "
                "Your hand slides down her silken belly into the humid heat between her thighs, finding her already slick and drenched with longing. "
                "She whimpers, grinding her hips into your palm with uninhibited hunger. 'Wanderer... please... I feel as though my entire soul is catching fire...'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_enter_tender_fwd",
                    text="Align your hips with hers and push smoothly into her velvet warmth.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_chantry_step3_dominant": DialogueNode(
            id="vanya_chantry_step3_dominant",
            speaker_name="Sister Vanya",
            text=(
                "You lift her onto the altar slab, her smooth bare thighs spreading wide in the candlelight. Stepping between them, you grasp her hips, "
                "your thumbs stroking the damp heat of her inner thighs. Her dark eyes darken with submission and desire. "
                "'Do with me as you will, wanderer,' she whispers raggedly. 'Cleanse me of this dreadful silence.' "
                "She watches with parted lips and heavy breathing as you unbuckle your trousers and position yourself against her soaking cleft."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_dom_to_step4",
                    text="Trace your palms along her trembling thighs into her soaked feminine core.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_enter_dom",
                    text="Thrust deeply into her tight, glistening depths with fierce, possessive rhythm.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_foreplay_dominant": DialogueNode(
            id="vanya_eroge_foreplay_dominant",
            speaker_name="Sister Vanya",
            text=(
                "You lift her onto the altar slab, her smooth bare thighs spreading wide in the candlelight. Stepping between them, you grasp her hips, "
                "your thumbs stroking the damp heat of her inner thighs. Her dark eyes darken with submission and desire. "
                "'Do with me as you will, wanderer,' she whispers raggedly. 'Cleanse me of this dreadful silence.' "
                "She watches with parted lips and heavy breathing as you unbuckle your trousers and position yourself against her soaking cleft."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_enter_dom_fwd",
                    text="Thrust deeply into her tight, glistening depths with fierce, possessive rhythm.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_chantry_step3_oral": DialogueNode(
            id="vanya_chantry_step3_oral",
            speaker_name="Sister Vanya",
            text=(
                "Kneeling between her trembling, parted thighs, your hands slide up to cup her soft buttocks, drawing her hips forward over the altar edge. "
                "Her feminine folds glisten with nectar in the warm candlelight. When your tongue traces along her swollen clitoris and laps at her soaking entrance, "
                "Vanya cries out in sheer disbelief, her fingers tangling frantically in your hair as her hips buck upward against your mouth. "
                "'Merciful martyrs... ah, wanderer! Yes! Don't stop... I cannot bear how sweet it feels!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_oral_to_step4",
                    text="Caress her slick inner thighs and gently part her glistening folds further.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_oral_to_climax",
                    text="Rise up and prepare to sheath your rigid length inside her drenched core.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_foreplay_oral": DialogueNode(
            id="vanya_eroge_foreplay_oral",
            speaker_name="Sister Vanya",
            text=(
                "Kneeling between her trembling, parted thighs, your hands slide up to cup her soft buttocks, drawing her hips forward over the altar edge. "
                "Her feminine folds glisten with nectar in the warm candlelight. When your tongue traces along her swollen clitoris and laps at her soaking entrance, "
                "Vanya cries out in sheer disbelief, her fingers tangling frantically in your hair as her hips buck upward against your mouth. "
                "'Merciful martyrs... ah, wanderer! Yes! Don't stop... I cannot bear how sweet it feels!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_oral_alias_fwd",
                    text="Rise up and prepare to sheath your rigid length inside her drenched core.",
                    next_node="vanya_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 4: Intimate Caresses & Lubrication
        "vanya_chantry_step4_caress": DialogueNode(
            id="vanya_chantry_step4_caress",
            speaker_name="Sister Vanya",
            text=(
                "Rising to your feet, your fingers glide through her dripping cleft, finding her burning with fevered, unbearable need. "
                "Vanya's hips undulate eagerly against your palm, her breathing ragged and needy as slick nectar coats your fingers and drips onto the altar stone. "
                "'Wanderer... please... my body is on fire...' she gasps, reaching down to trace the rigid steel of your shaft. "
                "'I need to feel you inside me. Don't make me wait another breath.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step5",
                    text="Align your hardening shaft against her weeping entrance and prepare to enter.",
                    next_node="vanya_chantry_step5_entry",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 5: Penetration & Alignment
        "vanya_chantry_step5_entry": DialogueNode(
            id="vanya_chantry_step5_entry",
            speaker_name="Sister Vanya",
            text=(
                "Unbuckling your trousers, you press your rigid head against her glistening aperture. With a slow, deliberate thrust, you breach her snug sheath. "
                "Her tight inner walls stretch to accommodate your girth, drawing a long, shuddering gasp from her lips as you sink smoothly to the root. "
                "Vanya wraps her arms tightly around your neck, weeping softly in overwhelmed gratification as she takes every inch of your length into her velvet heat."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step6",
                    text="Pause to let her adjust to your fullness before establishing a slow, deep rhythm.",
                    next_node="vanya_chantry_step6_rhythm",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 6: Initial Cadence & Deep Friction
        "vanya_chantry_step6_rhythm": DialogueNode(
            id="vanya_chantry_step6_rhythm",
            speaker_name="Sister Vanya",
            text=(
                "Holding her waist firmly, you begin a deep, measured cadence. Each long stroke pulls your length almost clear before plunging back into her feverish depths. "
                "Her velvet walls clamp greedily around your shaft, milking every inch with involuntary suction. "
                "Vanya's breathless whimpers echo in the quiet crypt as her hips meet yours in hypnotic, wet friction, her eyes swimming with adoration."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step7",
                    text="Hook her legs over your hips and increase the depth of each thrust.",
                    next_node="vanya_chantry_step7_shift",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 7: Positional Shift & Escalation
        "vanya_chantry_step7_shift": DialogueNode(
            id="vanya_chantry_step7_shift",
            speaker_name="Sister Vanya",
            text=(
                "Lifting her slender legs higher, you alter the angle of entry to strike her deepest, most sensitive nerves. "
                "Wet rhythmic slaps resound against the altar stones as your pelvic bones meet. "
                "Vanya's cries become higher, more desperate, her fingernails digging through your tunic as she arches her spine into every driving impact."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step8",
                    text="Pick up the tempo into a fierce, relentless pace.",
                    next_node="vanya_chantry_step8_frenzy",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 8: Fierce Cadence & Vocal Surrender
        "vanya_chantry_step8_frenzy": DialogueNode(
            id="vanya_chantry_step8_frenzy",
            speaker_name="Sister Vanya",
            text=(
                "Your thrusts turn frantic, possessive, and heavy. Both bodies are bathed in glistening sweat, chests crashing together with bruising fervor. "
                "Vanya abandons all reserve, tossing her head as her dark hair fans across the altar, calling out your name in unrestrained, wanton moans "
                "that drown out the tolling bell above. 'Ah... yes! Harder, my love... take all of me!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step9",
                    text="Drive relentlessly toward the edge, feeling her walls flutter and tighten.",
                    next_node="vanya_chantry_step9_precipice",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 9: The Precipice / Edging
        "vanya_chantry_step9_precipice": DialogueNode(
            id="vanya_chantry_step9_precipice",
            speaker_name="Sister Vanya",
            text=(
                "The summit approaches like a roaring inferno. Vanya's inner passage begins to convulse in violent pre-orgasmic tremors, "
                "squeezing your shaft with fierce, rhythmic contractions. Her breath hitches in ragged sobs of pleasure, her legs locking desperately around your waist. "
                "'I am coming... wanderer, oh gods, don't stop... right there!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_step10",
                    text="Thrust to the hilt with everything you have and surrender to the explosive climax.",
                    next_node="vanya_chantry_step10_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 10: Explosive Climax
        "vanya_chantry_step10_climax": DialogueNode(
            id="vanya_chantry_step10_climax",
            speaker_name="Sister Vanya",
            text=(
                "Driving to the absolute root with overwhelming power, you trigger a violent, toe-curling climax that shatters through both of you. "
                "Vanya screams into your shoulder, her body coiling and spasming in pure transcendent bliss as her tight core milks you relentlessly. "
                "A guttural roar tears from your throat as you pump voluminous waves of boiling release deep within her womb, collapsing together in spent, breathless surrender."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_chantry_to_afterglow",
                    text="Hold her tightly against your chest as your breathing slows in the warm candlelight.",
                    next_node="vanya_chantry_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Sister Vanya's Embroidered Rosary"
                ),
                # Aliases for existing tests
                DialogueChoice(
                    id="c_vanya_eroge_afterglow",
                    text="Hold her gently as your breathing slows in the warm candlelight.",
                    next_node="vanya_chantry_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Sister Vanya's Embroidered Rosary"
                )
            ]
        ),
        "vanya_eroge_climax": DialogueNode(
            id="vanya_eroge_climax",
            speaker_name="Sister Vanya",
            text=(
                "Driving to the absolute root with overwhelming power, you trigger a violent, toe-curling climax that shatters through both of you. "
                "Vanya screams into your shoulder, her body coiling and spasming in pure transcendent bliss as her tight core milks you relentlessly. "
                "A guttural roar tears from your throat as you pump voluminous waves of boiling release deep within her womb, collapsing together in spent, breathless surrender."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_afterglow_alias",
                    text="Hold her gently as your breathing slows in the warm candlelight.",
                    next_node="vanya_chantry_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Sister Vanya's Embroidered Rosary"
                )
            ]
        ),
        # Afterglow & Bonding
        "vanya_chantry_afterglow": DialogueNode(
            id="vanya_chantry_afterglow",
            speaker_name="Sister Vanya",
            text=(
                "Wrapped together in the heavy chantry vestments on the crypt floor, Vanya's head rests against your bare chest, her fingers lazily tracing "
                "the executioner's brand on your neck. A peaceful, radiant smile touches her lips—all terror of the purge banished into complete calm. "
                "'I never knew such devotion existed,' she murmurs softly. She places a velvet cord holding her sanctified silver rosary around your neck. "
                "'Keep this. It is embroidered with the blessings of the Quiet Dawn. It will shield your mind from dread. Now, let me fight at your side.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_post_intimacy_recruit",
                    text="'You belong with me now, Vanya. Take up your chirurgeon kit and let us break through the perimeter.'",
                    next_node="vanya_recruited",
                    relationship_change=20
                ),
                DialogueChoice(
                    id="c_vanya_companion_return_hub",
                    text="Resume traveling together.",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_eroge_afterglow": DialogueNode(
            id="vanya_eroge_afterglow",
            speaker_name="Sister Vanya",
            text=(
                "Wrapped together in the heavy chantry vestments on the crypt floor, Vanya's head rests against your bare chest, her fingers lazily tracing "
                "the executioner's brand on your neck. A peaceful, radiant smile touches her lips—all terror of the purge banished into complete calm. "
                "'I never knew such devotion existed,' she murmurs softly. She places a velvet cord holding her sanctified silver rosary around your neck. "
                "'Keep this. It is embroidered with the blessings of the Quiet Dawn. It will shield your mind from dread. Now, let me fight at your side.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_post_intimacy_recruit_alias",
                    text="'You belong with me now, Vanya. Take up your chirurgeon kit and let us break through the perimeter.'",
                    next_node="vanya_recruited",
                    relationship_change=20
                ),
                DialogueChoice(
                    id="c_vanya_companion_return_hub_alias",
                    text="Resume traveling together.",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_recruited": DialogueNode(
            id="vanya_recruited",
            speaker_name="Sister Vanya",
            text=(
                "Vanya straps an apothecary satchel across her chest and conceals a surgical scalpel in her sleeve. Her eyes shine with total devotion. "
                "'My place is at your side, my love. I will mend your flesh when you bleed, and strike when darkness closes in.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_recruited_to_hub",
                    text="'Let us move together, Vanya. Stay close to me.'",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        # --- Sister Vanya Companion Party Dialogue Hub & Interactions ---
        "vanya_companion_hub": DialogueNode(
            id="vanya_companion_hub",
            speaker_name="Sister Vanya",
            text=(
                "Vanya walks close by your side amidst the drifting soot, her dark eyes shining with tender, unwavering devotion. "
                "She has tied her habit back for swift movement, keeping a chirurgeon satchel and silver surgical scalpel secured at her hip. "
                "'I am with you, wanderer,' she whispers softly, her warm hand gently clasping your fingers. 'Whatever darkness awaits us in Oakhaven, we face it together.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_companion_talk",
                    text="Converse with Vanya about her thoughts and feelings.",
                    next_node="vanya_companion_talk"
                ),
                DialogueChoice(
                    id="c_vanya_companion_intimacy",
                    text="[Erotic Scene] Pull Vanya into a quiet, shadowed alcove for an intimate encounter.",
                    next_node="vanya_companion_intimacy_start",
                    is_intimacy_action=True,
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_vanya_companion_tend",
                    text="Ask Vanya to examine your cuts and soothe your trembling nerves (Triage Healing).",
                    next_node="vanya_companion_tend"
                ),
                DialogueChoice(
                    id="c_vanya_companion_dismiss",
                    text="'The road ahead is too hazardous, Vanya. Wait here until I return.'",
                    next_node="vanya_companion_dismiss"
                )
            ]
        ),
        "vanya_companion_talk": DialogueNode(
            id="vanya_companion_talk",
            speaker_name="Sister Vanya",
            text=(
                "Vanya gazes toward the hazy quarantine ramparts where the watchtower bell tolls ominously. "
                "'For so long, the Dawnshroud taught me that pain was penance and affection was corruption,' she admits, her voice trembling slightly. "
                "'Yet when you touch me, when we fight together... I feel clean. Truly clean. You gave me back my will to live, wanderer. I will not let you fall.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_comp_talk_intimacy",
                    text="Draw her into your arms. 'Let us take comfort in each other right now.'",
                    next_node="vanya_companion_intimacy_start",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_comp_talk_return",
                    text="'Stay sharp, Vanya. We have a city to escape.'",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_companion_intimacy_start": DialogueNode(
            id="vanya_companion_intimacy_start",
            speaker_name="Sister Vanya",
            text=(
                "Stepping behind a secluded curtain into a quiet, private space away from the cold night wind, you pull Vanya into the deep shadows. "
                "Her breathing quickens immediately as your hands settle upon her hips. Her dark eyes carry an intoxicating mix of shyness and wanton surrender. "
                "'Every moment with you feels like stolen grace,' she breathes, her fingers trembling as she unfastens the collar of her habit, "
                "exposing the smooth, pale curve of her throat and the soft swell of her breasts damp with perspiration. 'Touch me, wanderer... make me forget the ash and the flames.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_comp_to_location_scene",
                    text="Draw her close and undress together in the secluded darkness.",
                    next_node="vanya_chantry_step1_initiate",
                    is_intimacy_action=True
                ),
                # Aliases for compatibility
                DialogueChoice(
                    id="c_vanya_companion_oral",
                    text="Kneel before her, parting her habit and lifting her chemise to worship her wet core with your lips.",
                    next_node="vanya_companion_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_companion_coupling_direct",
                    text="Lift her against the wall, parting her smooth thighs and thrusting deep into her velvet heat.",
                    next_node="vanya_companion_coupling",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_companion_oral": DialogueNode(
            id="vanya_companion_oral",
            speaker_name="Sister Vanya",
            text=(
                "Kneeling on the cold flagstones, you slide your hands up the silk of her bare inner thighs, parting them wide in the sheltered gloom. "
                "Her intimate cleft is glistening, swollen, and radiating sweet heat. When your mouth descends upon her delicate folds, lapping and suckling at her sensitive pearl, "
                "Vanya gasps in helpless ecstasy. Her fingers bury deep into your hair, her hips arching instinctively upward against your mouth. "
                "'Ah... wanderer! Merciful martyrs... yes, right there! It is too much... I cannot bear how sweet it feels!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_companion_to_coupling",
                    text="Rise up, align your hardening shaft with her dripping entrance, and push in to the hilt.",
                    next_node="vanya_companion_coupling",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_companion_coupling": DialogueNode(
            id="vanya_companion_coupling",
            speaker_name="Sister Vanya",
            text=(
                "You hoist her slender thighs around your waist and press her back against the damp stone wall. With a slow, deliberate thrust, your rigid length slides smoothly into her snug, feverishly wet passage. "
                "Vanya lets out a stifled, wanton cry into the crook of your neck, her fingernails clawing through your tunic as her tight inner walls squeeze around you in exquisite spasms. "
                "Establishing a deep, forceful cadence, your hips meet hers with wet, rhythmic slaps that echo softly in the quiet alcove. Her breathless whimpers turn into needy, unrestrained moans as she clings to you with desperate fervor."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_companion_to_climax",
                    text="Accelerate the rhythm into a frantic, possessive surge and claim her ultimate release.",
                    next_node="vanya_companion_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_companion_climax": DialogueNode(
            id="vanya_companion_climax",
            speaker_name="Sister Vanya",
            text=(
                "Gripping her hips with bruising passion, you drive into her depths with unrelenting power. Vanya's body coils like a drawn bow before shattering into a violent, toe-curling climax. "
                "Her innermost muscles pulse and clamp greedily around your shaft, milking every tremor as she cries out your name in pure, transcendent surrender. "
                "Unable to hold back, a guttural groan tears from your throat as you bury yourself fully to the root, pumping copious waves of boiling release deep within her trembling womb. "
                "You hold her suspended against the wall as your pulses race in unison, the cold dread of Oakhaven completely washed away in overwhelming carnal bliss."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_companion_afterglow",
                    text="Lower her gently to her feet and hold her close in the quiet aftermath.",
                    next_node="vanya_companion_afterglow",
                    is_intimacy_action=True,
                    relationship_change=20
                )
            ]
        ),
        "vanya_companion_afterglow": DialogueNode(
            id="vanya_companion_afterglow",
            speaker_name="Sister Vanya",
            text=(
                "Vanya leans heavily against your chest, her flushed face buried in your shoulder as she catches her ragged breath. A radiant, devoted smile spreads across her lips as she adjusts her habit. "
                "'With you beside me, wanderer, I fear neither the pyres nor the dark. My body and my soul belong to you.' (Dread purged to 0. Devotion absolute)."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_companion_return_hub",
                    text="Resume traveling together.",
                    next_node="vanya_companion_hub"
                )
            ]
        ),

        # --- Sister Vanya 10-Step Erotic Sequence: The Gilded Rat (Location Unique Scene) ---
        # Step 1: Initiating in the Pleasure Den
        "vanya_gilded_step1_initiate": DialogueNode(
            id="vanya_gilded_step1_initiate",
            speaker_name="Sister Vanya",
            text=(
                "Leading Vanya into an opulent, curtained alcove of the Gilded Rat Parlour, you shut out the noise of the tavern. "
                "Deep red silk drapes seal the room in an intoxicating haze of burned sandalwood, opium, and spilled wine. "
                "The devout sister stands amidst the plush velvet divans and carved brass lanterns, her cheeks burning with an intense crimson blush. "
                "'I never imagined I would set foot in such a place of indulgence,' she murmurs, her trembling fingers reaching for her wimple. "
                "'Yet here with you, amidst all this forbidden warmth... I feel my pious vows dissolving like mist.' "
                "She unpins the white cloth, letting her dark, raven tresses cascade luxuriously over her bare shoulders."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step2",
                    text="Unbutton her habit and lay her back onto the opulent red velvet cushions.",
                    next_node="vanya_gilded_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        # Step 2: Foreplay & Branching Choices (Gilded Rat)
        "vanya_gilded_step2_foreplay": DialogueNode(
            id="vanya_gilded_step2_foreplay",
            speaker_name="Sister Vanya",
            text=(
                "Her austere habit falls to the carpet, leaving Vanya reclining in her damp linen chemise across the sea of down pillows. "
                "The decadent surroundings seem to embolden her hidden passions; her eyes darken with longing as she looks up at you. "
                "Her breasts heave against the translucent fabric, taut rose nipples straining eagerly for your touch."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_branch_wine",
                    text="[Spiced Plum Wine] Share a mouthful of rich plum wine, letting sweet vintage trickle down her throat and breasts.",
                    next_node="vanya_gilded_step3_wine",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_gilded_branch_oral",
                    text="[Decadent Oral Worship] Part her silk-cushioned thighs and bury your face into her glistening, weeping core.",
                    next_node="vanya_gilded_step3_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_gilded_branch_dominant",
                    text="[Commanding Seduction] Pin her wrists into the down bolsters, claiming her body with fierce, dominant possession.",
                    next_node="vanya_gilded_step3_dominant",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 3: Deepening Foreplay (Branch Outcomes)
        "vanya_gilded_step3_wine": DialogueNode(
            id="vanya_gilded_step3_wine",
            speaker_name="Sister Vanya",
            text=(
                "Taking a sip of spiced plum wine from a crystal goblet, you seal your mouth over Vanya's parting lips, passing the burning sweet vintage between you. "
                "A wanton whimper vibrates in her throat. Drops of ruby wine spill down her chin and trickle into the valley of her cleavage. "
                "Your mouth follows the warm trail, lapping the spiced wine from her skin and suckling her taut nipples. "
                "Vanya arches off the cushions with an intoxicating moan, her fingers digging desperately into your hair."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_wine_to_step4",
                    text="Slide your hand down between her bare thighs into the pool of humid heat.",
                    next_node="vanya_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_gilded_step3_oral": DialogueNode(
            id="vanya_gilded_step3_oral",
            speaker_name="Sister Vanya",
            text=(
                "Kneeling on the lavish rug between her parted thighs, you lift her hips onto a silk bolster. Her feminine cleft is glistening, swollen, and radiating sweet perfume. "
                "When your tongue parts her outer petals to lap and suckle at her hypersensitive pearl, Vanya gasps in sheer disbelief. "
                "Her pious composure disintegrates completely into wanton, breathy cries as her hips buck upward against your mouth, soaking your lips in honeyed nectar."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_oral_to_step4",
                    text="Caress her trembling thighs and prepare her body for full entry.",
                    next_node="vanya_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_gilded_step3_dominant": DialogueNode(
            id="vanya_gilded_step3_dominant",
            speaker_name="Sister Vanya",
            text=(
                "Pinning her wrists above her head into the crimson down pillows, you press your heavy frame over her slender body. "
                "Her dark eyes shine with wanton surrender as you bite lightly along the sensitive curve of her throat and nip her earlobe. "
                "'Take me, wanderer,' she whispers raggedly, trembling with submission. 'Corrupt every sacred thought I ever had... make me only yours.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_dom_to_step4",
                    text="Release her hands and slide your fingers deep into her soaking entrance.",
                    next_node="vanya_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 4: Intimate Caresses & Lubrication
        "vanya_gilded_step4_caress": DialogueNode(
            id="vanya_gilded_step4_caress",
            speaker_name="Sister Vanya",
            text=(
                "Your fingers probe the depths of her soaked passage, discovering her burning with uninhibited, fevered arousal. "
                "Vanya's hips roll sinuously against your palm, her inner walls fluttering around your fingers with hot, eager friction. "
                "Her breath comes in rapid pants, her face flushed with decadent desire. 'Please, my love... no more teasing... sheath yourself inside me!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step5",
                    text="Position your rigid length at her dripping entrance and slide smoothly inside.",
                    next_node="vanya_gilded_step5_entry",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 5: Penetration on the Velvet Divan
        "vanya_gilded_step5_entry": DialogueNode(
            id="vanya_gilded_step5_entry",
            speaker_name="Sister Vanya",
            text=(
                "Guiding your throbbing shaft between her slick folds, you push forward with a slow, deliberate motion. "
                "Her tight, velvety core yields to your broad head, stretching snugly around your girth until your hips meet with a soft, wet impact. "
                "Vanya cries out in breathless ecstasy, her fingernails scoring your bare shoulders as her inner muscles clamp eagerly around you to the hilt."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step6",
                    text="Pause to savor her tight warmth before establishing a deep, rolling tempo.",
                    next_node="vanya_gilded_step6_rhythm",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 6: Sinuous Cadence on Crimson Silks
        "vanya_gilded_step6_rhythm": DialogueNode(
            id="vanya_gilded_step6_rhythm",
            speaker_name="Sister Vanya",
            text=(
                "The plush mattress gives way beneath your bodies as you begin a slow, rhythmic cadence. "
                "Every deep, measured stroke draws a wanton gasp from Vanya's lips. Her hips roll in decadent synergy with yours, meeting each thrust with increasing eagerness. "
                "The sweet smell of opium and her own aroused scent fills the curtained alcove, heightening every point of contact into pure delirium."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step7",
                    text="Pull her hips to the edge of the cushions to drive even deeper.",
                    next_node="vanya_gilded_step7_shift",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 7: Positional Shift & Intensifying Depth
        "vanya_gilded_step7_shift": DialogueNode(
            id="vanya_gilded_step7_shift",
            speaker_name="Sister Vanya",
            text=(
                "Hooking her slender legs over your hips, you draw her lower body to the edge of the velvet bolsters, driving home at a steeper, devastating angle. "
                "Wet, rhythmic slaps resound through the silk-draped chamber. Vanya arches her back, her full breasts trembling with each impact, "
                "her cries turning melodic and unrestrained as you graze the most sensitive nerve clusters of her womb."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step8",
                    text="Quicken the tempo into a fierce, breathless pounding.",
                    next_node="vanya_gilded_step8_frenzy",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 8: Fierce Cadence & Sensual Frenzy
        "vanya_gilded_step8_frenzy": DialogueNode(
            id="vanya_gilded_step8_frenzy",
            speaker_name="Sister Vanya",
            text=(
                "Your hips crash against hers with unrelenting, commanding power. Sweat slicks both your chests, gleaming in the amber glow of the brass lantern. "
                "Vanya abandons all reserve, clutching your neck and whispering wanton words of devotion into your ear. "
                "Her cries rise above the muffled laughter of the distant parlour, celebrating the raw, uninhibited joy of the flesh."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step9",
                    text="Drive into her with everything you have, feeling her walls begin to convulse.",
                    next_node="vanya_gilded_step9_precipice",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 9: The Precipice / Pre-Climax
        "vanya_gilded_step9_precipice": DialogueNode(
            id="vanya_gilded_step9_precipice",
            speaker_name="Sister Vanya",
            text=(
                "The peak rushes over both of you like a fevered tidal wave. Vanya's inner passage contracts with furious, rhythmic spasms, "
                "milking your swollen length with desperate suction. Her nails bite into your back as her toes curl into the silk sheets. "
                "'I cannot hold back! Ah... wanderer, take me... fill me now!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_step10",
                    text="Thrust to the root one final time and surrender to the explosive release.",
                    next_node="vanya_gilded_step10_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 10: Explosive Climax in the Boudoir
        "vanya_gilded_step10_climax": DialogueNode(
            id="vanya_gilded_step10_climax",
            speaker_name="Sister Vanya",
            text=(
                "With a final, shattering plunge, you bury yourself to the very hilt within her drenched depths. "
                "Vanya lets out a breathless, quivering scream into your shoulder as an earth-shattering orgasm rips through her body, "
                "her inner walls fluttering in violent, unending spasms. With a guttural roar, you flood her deep within with hot, pulsing release, "
                "pumping copious warmth into her trembling womb as you collapse together into the disheveled crimson silks."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_to_afterglow",
                    text="Hold her closely as your ragged breathing settles amidst the silk cushions.",
                    next_node="vanya_gilded_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        # Afterglow (Gilded Rat)
        "vanya_gilded_afterglow": DialogueNode(
            id="vanya_gilded_afterglow",
            speaker_name="Sister Vanya",
            text=(
                "Wrapped in a warm silk mantle upon the crimson divan, Vanya rests her flushed face against your chest, tracing your jawline with a tender, lazy smile. "
                "'I used to believe holiness was found only in deprivation and cold stone,' she whispers softly, her eyes shining with absolute devotion. "
                "'Tonight you showed me that true transcendence is found in love and desire. I fear nothing while I am yours.' "
                "(All dread eradicated. Devotion absolute)."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_gilded_return_hub",
                    text="Adjust your clothing and return to the parlour together.",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_companion_tend": DialogueNode(
            id="vanya_companion_tend",
            speaker_name="Sister Vanya",
            text=(
                "Vanya unrolls clean linen strips from her apothecary pouch and uncorks an amber vial of distilled willow-bark antiseptic. "
                "With tender, expert hands, she cleans your grime-caked cuts and secures fresh dressings across your wounds. "
                "As she works, her gentle breath tickles your neck, soothing your frayed mind. (+15 HP, -10 Dread)."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_tend_return",
                    text="'Thank you, Vanya. Let us proceed.'",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_companion_dismiss": DialogueNode(
            id="vanya_companion_dismiss",
            speaker_name="Sister Vanya",
            text=(
                "Vanya looks at you with sorrow, but nods with quiet dignity. "
                "'I understand, wanderer. I will return to the Chantry and care for the wounded until you call for me again. Stay alive... for my sake.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_confirm_dismiss",
                    text="Watch her slip back toward the Chantry shadows.",
                    next_node="vanya_companion_dismiss_final"
                ),
                DialogueChoice(
                    id="c_vanya_cancel_dismiss",
                    text="'Never mind, Vanya. Stay with me.'",
                    next_node="vanya_companion_hub"
                )
            ]
        ),
        "vanya_companion_dismiss_final": DialogueNode(
            id="vanya_companion_dismiss_final",
            speaker_name="Sister Vanya",
            text="Vanya slips into the fog, returning to the Ruined Chantry.",
            choices=[]
        ),
        "vanya_hostile": DialogueNode(
            id="vanya_hostile",
            speaker_name="Sister Vanya",
            text=(
                "Her eyes harden like flint. She grips an alchemical fire flask from her belt. 'Then burn with the rest of the scum!' she snarls. "
                "Her hatred for you is now absolute."
            ),
            choices=[]
        )
    }

    malakor_dialogues = {
        "root": DialogueNode(
            id="root",
            speaker_name="Commander Malakor",
            text=(
                "Malakor sits atop an upturned ale barrel, methodically wiping fresh gore from a notched greatsword. "
                "His broad chest is bound in battered cuirass and scarred with jagged blade wounds. Piercing amber eyes look you up and down, "
                "assessing your build and stance. 'Another stray dog sniffing around my bastion. State your business before I carve you into dog meat.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_sinew",
                    text="[Sinew 14] Slam your fist against his iron barricade without flinching. 'I don't bark, Malakor. And I don't crawl.'",
                    next_node="malakor_sinew_success",
                    required_stat="sinew",
                    required_value=14,
                    relationship_change=15,
                    failure_node="malakor_sinew_fail"
                ),
                DialogueChoice(
                    id="c_malakor_spar",
                    text="'They say the Iron Drakes fight for gold, but you fight for blood. Let's test our steel in the pit.'",
                    next_node="malakor_spar_challenge",
                    relationship_change=10
                ),
                DialogueChoice(
                    id="c_malakor_vanya_quest",
                    text="'Sister Vanya needs the Wolfsbane Nectar you looted from the chantry. Name your price.'",
                    next_node="malakor_quest_trade",
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_malakor_court",
                    text="Meet his gaze directly, a slow smirk touching your lips. 'A warrior of your caliber shouldn't waste his final hours brooding alone in the dirt.'",
                    next_node="malakor_romance_start",
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_malakor_threat",
                    text="'Hand over the keys and the nectar, you mercenary filth, or I'll feed you your own sword.'",
                    next_node="malakor_hostile",
                    relationship_change=-35,
                    faction_changes={"iron_drakes": -20},
                    is_hostile_action=True
                )
            ]
        ),
        "malakor_spar_challenge": DialogueNode(
            id="malakor_spar_challenge",
            speaker_name="Commander Malakor",
            text=(
                "A savage grin splits the veteran's scarred face. He tosses aside his whetstone and picks up a blunted iron broadsword. "
                "'A challenger with guts! Step into the pit, wanderer. Let's see if your backbone is made of iron or rotten timber!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_spar_sinew",
                    text="[Sinew 13] Meet his overhead crash head-on, locking blades and throwing him off balance.",
                    next_node="malakor_spar_win",
                    required_stat="sinew",
                    required_value=13,
                    relationship_change=20,
                    item_reward="Heavy Whetstone"
                ),
                DialogueChoice(
                    id="c_malakor_spar_guile",
                    text="[Guile 12] Duck beneath his sweeping swing and plant your boot in the crook of his knee.",
                    next_node="malakor_spar_win",
                    required_stat="guile",
                    required_value=12,
                    relationship_change=20,
                    item_reward="Heavy Whetstone"
                ),
                DialogueChoice(
                    id="c_malakor_spar_decline",
                    text="'Save your strength for the gate guards, Malakor. Let's talk business.'",
                    next_node="malakor_quest_trade"
                )
            ]
        ),
        "malakor_spar_win": DialogueNode(
            id="malakor_spar_win",
            speaker_name="Commander Malakor",
            text=(
                "The clash echoes off the brewery stone! Malakor stumbles back, catching his footing with a hearty, booming roar of laughter. "
                "'Hah! True iron! By the Drakes, it's been months since a man stood in front of my blade without wetting his trousers! "
                "Take this heavy whetstone from my forge—you've earned the Drakes' warrior respect, brother.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_spar_to_quest",
                    text="'What keeps a warrior like you waiting in this slaughterhouse?'",
                    next_node="malakor_personal_quest"
                )
            ]
        ),
        "malakor_sinew_success": DialogueNode(
            id="malakor_sinew_success",
            speaker_name="Commander Malakor",
            text=(
                "Malakor lets out a guttural, appreciative chuckle. The heavy greatsword rests at ease against his knee. "
                "'Iron in your spine. Rare in this rotting sinkhole. Most men drop to their knees and beg for a transit badge. "
                "I respect steel that doesn't bend.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_quest_hook",
                    text="'What keeps a commander like you in this doomed town instead of fleeing beyond the wall?'",
                    next_node="malakor_personal_quest",
                    relationship_change=10
                )
            ]
        ),
        "malakor_sinew_fail": DialogueNode(
            id="malakor_sinew_fail",
            speaker_name="Commander Malakor",
            text=(
                "Malakor scoffs, knocking your hand aside with the flat of his pommel. 'Weak grip. You talk like an executioner but hit like a novice. "
                "Try that again and you won't leave this courtyard alive.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_back_from_fail",
                    text="'Let's discuss business.'",
                    next_node="malakor_quest_trade"
                )
            ]
        ),
        "malakor_personal_quest": DialogueNode(
            id="malakor_personal_quest",
            speaker_name="Commander Malakor",
            text=(
                "A shadow of raw, suppressed grief crosses the veteran's scarred face. 'My younger brother, Loras. He was trapped in the lower quarter "
                "when the Dawnshroud zealots barricaded the street and torched the houses. He carried our family's signet ring—the last scrap of honor "
                "we owned. The pyre in the Gallow-Square is where they dumped the ashes. Find Loras's Iron Signet, and I will give you anything you want: "
                "my wolfsbane, my steel, or an escape route.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_accept_quest",
                    text="'I will recover your brother's signet from the ash.'",
                    next_node="malakor_quest_accepted",
                    relationship_change=15,
                    quest_trigger="q_blood_brass",
                    quest_stage_set=1
                )
            ]
        ),
        "malakor_quest_accepted": DialogueNode(
            id="malakor_quest_accepted",
            speaker_name="Commander Malakor",
            text=(
                "'Search the corpse-urns near the gibbets in the Gallow-Square. Watch for the ghouls and zealot sentries. Don't die on me.'"
            ),
            choices=[]
        ),
        "malakor_quest_trade": DialogueNode(
            id="malakor_quest_trade",
            speaker_name="Commander Malakor",
            text=(
                "'Vanya wants my poison? She's got bleeding heart disease. Still, I don't give away goods for free. Bring me my brother's signet "
                "from the Gallow-Square pyre, or pay me 25 Sovereigns upfront.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_pay_25",
                    text="Pay 25 Sovereigns for the Wolfsbane Nectar.",
                    next_node="malakor_paid_nectar",
                    item_reward="Wolfsbane Nectar",
                    sovereign_cost=25,
                    relationship_change=10,
                    quest_trigger="q_mercy_hemlock",
                    quest_stage_set=2
                ),
                DialogueChoice(
                    id="c_malakor_take_quest_alt",
                    text="'Tell me about your brother. I will find the signet.'",
                    next_node="malakor_personal_quest"
                )
            ]
        ),
        "malakor_paid_nectar": DialogueNode(
            id="malakor_paid_nectar",
            speaker_name="Commander Malakor",
            text=(
                "Malakor pockets the coin with a grunt and slides a heavy, wax-sealed cobalt flask across the iron table. "
                "'Take it. Enough hemlock and wolfsbane in there to put down an ox. Tell the little sister not to waste it.'"
            ),
            choices=[]
        ),
        "malakor_quest_complete": DialogueNode(
            id="malakor_quest_complete",
            speaker_name="Commander Malakor",
            text=(
                "Malakor holds the scorched, blood-encrusted signet ring in his trembling, calloused fingers. A heavy sigh rattles in his chest, "
                "years of martial stoicism threatening to fracture. 'Loras... forgive me.' He looks at you with fierce, unwavering respect. "
                "'You kept your word when nobody in this cursed world does. The Wolfsbane Nectar is yours, and so is my debt.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_embrace",
                    text="Clasp his forearm in an iron warrior's grip. 'Your brother's honor lives on in you, Malakor. Stand with me.'",
                    next_node="malakor_intimacy_scene",
                    relationship_change=25
                ),
                DialogueChoice(
                    id="c_malakor_recruit",
                    text="'Stand with me, Commander. Join my party and let us carve our way out together.'",
                    next_node="malakor_recruited",
                    relationship_change=15
                )
            ]
        ),
        "malakor_romance_start": DialogueNode(
            id="malakor_romance_start",
            speaker_name="Commander Malakor",
            text=(
                "Malakor's eyes widen slightly before a rugged, wolfish grin creeps onto his battle-hardened jaw. "
                "'Bold words for a wanderer. Most men fear what my hands can do. But you... you look at me like an equal in the field. "
                "Prove you have the stomach to ride the storm with me, and maybe I'll show you what Iron Drake brotherhood truly means.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_romance_hook",
                    text="'Give me a task to prove it, then.'",
                    next_node="malakor_personal_quest",
                    relationship_change=10
                )
            ]
        ),
        "malakor_intimacy_scene": DialogueNode(
            id="malakor_intimacy_scene",
            speaker_name="Commander Malakor",
            text=(
                "In his private armory surrounded by iron, trophies, and kegs of harsh rye gin, Malakor sets two heavy brass goblets on an anvil. "
                "He unsheathes a ceremonial hunting knife, slicing his palm before handing the hilt to you. "
                "You slice yours without hesitation. Grasping hands in an unyielding blood-grip, red rivulets mingle over the iron anvil. "
                "'Blood calls to blood,' Malakor growls with profound reverence. 'From this hour until the pyres turn cold, you are my war-brother.' "
                "He presents you with his Drake Whetstone—a prized relic that permanently sharpens your weapons for lethal combat damage."
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_post_intimacy_recruit",
                    text="'Get your greatsword, Malakor. Tonight, we fight as one.'",
                    next_node="malakor_recruited",
                    relationship_change=20,
                    item_reward="Malakor's Drake Whetstone"
                )
            ]
        ),
        "malakor_recruited": DialogueNode(
            id="malakor_recruited",
            speaker_name="Commander Malakor",
            text=(
                "Malakor hoists his greatsword, buckling his war belt with renewed purpose. 'I'm with you to the end of the line, brother. "
                "Anyone stands between us and the gates gets split from crown to groin.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_recruited_to_hub",
                    text="'Let us move, Commander. Check your perimeter.'",
                    next_node="malakor_companion_hub"
                )
            ]
        ),
        # --- Commander Malakor Companion Party Dialogue Hub & Interactions ---
        "malakor_companion_hub": DialogueNode(
            id="malakor_companion_hub",
            speaker_name="Commander Malakor",
            text=(
                "Malakor walks with heavy, purposeful strides at your flank, his massive Drake greatsword balanced easily upon his armored shoulder. "
                "His amber eyes constantly sweep the dark rooftops, anticipating Dawnbound ambushes. "
                "'Keep your guard up, brother,' he grunts, spitting blood into the ash. 'The purge bell is ticking, but anyone who crosses our path tonight will taste iron.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_companion_talk",
                    text="Converse with Malakor about his mercenary brotherhood and past battles.",
                    next_node="malakor_companion_talk"
                ),
                DialogueChoice(
                    id="c_malakor_companion_tactics",
                    text="Review combat tactics and coordinating strikes (Combat Advice).",
                    next_node="malakor_companion_tactics"
                ),
                DialogueChoice(
                    id="c_malakor_companion_drink",
                    text="Pass a flask of harsh rye gin and share a grim toast to survival.",
                    next_node="malakor_companion_drink"
                ),
                DialogueChoice(
                    id="c_malakor_companion_dismiss",
                    text="'Commander, hold your ground here while I scout ahead alone.'",
                    next_node="malakor_companion_dismiss"
                )
            ]
        ),
        "malakor_companion_talk": DialogueNode(
            id="malakor_companion_talk",
            speaker_name="Commander Malakor",
            text=(
                "Malakor gives a low, rumbling chuckle that rattles his steel cuirass. "
                "'I fought for the Iron Drakes across seven provinces, wanderer. Seen kings turn to worms and fortresses crumble to ash. "
                "Most men fight for coin, titles, or women. But when the sky catches fire, all that matters is having someone at your back who won't break. "
                "You brought Loras's signet home. That makes you blood to me. We die on our feet tonight, or we walk out those gates as brothers.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_talk_return",
                    text="'Well said, Malakor. Back to the front.'",
                    next_node="malakor_companion_hub"
                )
            ]
        ),
        "malakor_companion_tactics": DialogueNode(
            id="malakor_companion_tactics",
            speaker_name="Commander Malakor",
            text=(
                "Malakor points out an unarmored seam below the shoulder pauldron of standard Dawnbound plate. "
                "'If an inquisitor locks blades with you, don't try to bash their shield. Hook their knee, turn your shoulder, and drive your blade upward. "
                "Keep your Sinew behind your follow-through and let your momentum carry the strike.' (+2 combat readiness)."
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_tactics_return",
                    text="'Understood. Let us move.'",
                    next_node="malakor_companion_hub"
                )
            ]
        ),
        "malakor_companion_drink": DialogueNode(
            id="malakor_companion_drink",
            speaker_name="Commander Malakor",
            text=(
                "Malakor unslings a battered tin flask and takes a deep draught before tossing it to you. The harsh rye spirit burns like liquid embers down your throat, "
                "clearing the sulfur taste of Oakhaven. 'To blood, iron, and surviving the damned night,' he grunts, wiping his jaw. (-5 Dread)."
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_drink_return",
                    text="'To survival.'",
                    next_node="malakor_companion_hub"
                )
            ]
        ),
        "malakor_companion_dismiss": DialogueNode(
            id="malakor_companion_dismiss",
            speaker_name="Commander Malakor",
            text=(
                "Malakor plants his greatsword into the ground with a thud, nodding gravely. "
                "'Understood, wanderer. I'll hold the line at the Iron Bastion. If the Dawnbound try to overrun this sector before you get back, they'll find Drake steel waiting for them.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_confirm_dismiss",
                    text="Watch him turn back toward the Iron Bastion.",
                    next_node="malakor_companion_dismiss_final"
                ),
                DialogueChoice(
                    id="c_malakor_cancel_dismiss",
                    text="'Change of plans. Stay with me, Commander.'",
                    next_node="malakor_companion_hub"
                )
            ]
        ),
        "malakor_companion_dismiss_final": DialogueNode(
            id="malakor_companion_dismiss_final",
            speaker_name="Commander Malakor",
            text="Commander Malakor returns to the Iron Drake Bastion.",
            choices=[]
        ),
        "malakor_hostile": DialogueNode(
            id="malakor_hostile",
            speaker_name="Commander Malakor",
            text=(
                "Malakor draws his greatsword with a sickening hiss of sharpened steel. 'Dead man talking. I'll mount your skull above the gate!'"
            ),
            choices=[]
        )
    }

    silve_dialogues = {
        "root": DialogueNode(
            id="root",
            speaker_name="Madame Silve",
            text=(
                "Lounging on plush crimson cushions behind sheer silk veils, Madame Silve sips dark wine from a leaded crystal goblet. "
                "Her generous cleavage is accentuated by a corset of black lace and velvet; dark kohl lines her predatory, intelligent eyes. "
                "'Look at you,' she murmurs with a low, seductive purr. 'Muscles taut with panic, eyes searching for salvation. "
                "Everyone wants to leave Oakhaven tonight. What do your handsome lips desire, wanderer?'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_guile",
                    text="[Guile 12] Effortlessly slide onto the settee beside her, taking her wineglass to sip. 'I want your secret way out, Silve.'",
                    next_node="silve_guile_success",
                    required_stat="guile",
                    required_value=12,
                    relationship_change=15,
                    failure_node="silve_guile_fail"
                ),
                DialogueChoice(
                    id="c_silve_contraband",
                    text="'Show me what contraband your parlour peddles before the gates burn.'",
                    next_node="silve_contraband_shop",
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_silve_talk",
                    text="'I need transit through the Sluice Trench. They say you have the ear of the smugglers.'",
                    next_node="silve_info",
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_silve_flirt",
                    text="'I came looking for an escape, but staying here with you seems far more tempting.'",
                    next_node="silve_romance_start",
                    is_romance_action=True,
                    relationship_change=15
                )
            ]
        ),
        "silve_contraband_shop": DialogueNode(
            id="silve_contraband_shop",
            speaker_name="Madame Silve",
            text=(
                "Silve smiles seductively, gesturing to an inlaid cedar chest behind the bar. "
                "'Opium, vintage spiced plum wine, or medical bandages looted from dead merchants. Coin talks, darling.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_buy_wine",
                    text="Buy Spiced Plum Wine (10 Sovereigns) [Restores 12 HP, -15 Dread].",
                    next_node="silve_bought_item",
                    item_reward="Spiced Plum Wine",
                    sovereign_cost=10,
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_silve_buy_bandage",
                    text="Buy Purified Bandage (15 Sovereigns) [Restores 25 HP in combat].",
                    next_node="silve_bought_item",
                    item_reward="Purified Bandage",
                    sovereign_cost=15,
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_silve_shop_back",
                    text="'Let's speak of transit and the ledger.'",
                    next_node="silve_info"
                )
            ]
        ),
        "silve_bought_item": DialogueNode(
            id="silve_bought_item",
            speaker_name="Madame Silve",
            text=(
                "Silve passes the package with a teasing brush of her manicured fingers. 'A pleasure doing business with a man of taste.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_after_shop",
                    text="'Now, about the way beyond the walls.'",
                    next_node="silve_info"
                )
            ]
        ),
        "silve_guile_success": DialogueNode(
            id="silve_guile_success",
            speaker_name="Madame Silve",
            text=(
                "Silve laughs with genuine delight, tapping her manicured nails against your jawline. 'Quick hands, smooth tongue. "
                "I adore a man who knows how to take what he wants. The Sluice Trench is locked, darling. But Little Toby—the gutter rat— "
                "stole the grand master key and the Turnkey's Ledger. If you protect that boy and bring me the city ledger he carries, "
                "I will forge you an Imperial Pass that even the Grand Inquisitor cannot contest.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_accept_quest",
                    text="'I will secure the Turnkey Ledger from Toby.'",
                    next_node="silve_quest_accepted",
                    relationship_change=10,
                    quest_trigger="q_silk_cyanide",
                    quest_stage_set=1
                )
            ]
        ),
        "silve_guile_fail": DialogueNode(
            id="silve_guile_fail",
            speaker_name="Madame Silve",
            text=(
                "She smoothly pulls the glass away, eyes narrowing. 'Clumsy, darling. You almost spilled twenty-year vintage across my silk. "
                "Respect my parlour, or my bouncers will feed you to the canal eels.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_back_to_root",
                    text="'Let us talk of business instead.'",
                    next_node="silve_info"
                )
            ]
        ),
        "silve_info": DialogueNode(
            id="silve_info",
            speaker_name="Madame Silve",
            text=(
                "'Information costs either blood or coin. The Trench requires a special key held by Little Toby in Gallow-Square. "
                "Bring me the boy's stolen Turnkey Ledger, and I will make you a free man.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_accept_info",
                    text="'I will retrieve it.'",
                    next_node="silve_quest_accepted",
                    quest_trigger="q_silk_cyanide",
                    quest_stage_set=1
                )
            ]
        ),
        "silve_quest_accepted": DialogueNode(
            id="silve_quest_accepted",
            speaker_name="Madame Silve",
            text=(
                "'Hurry, lover. The midnight bells won't wait for your slow feet.'"
            ),
            choices=[]
        ),
        "silve_romance_start": DialogueNode(
            id="silve_romance_start",
            speaker_name="Madame Silve",
            text=(
                "She leans into your chest, her perfumed hair brushing your collarbone as she traces the executioner's mark on your neck. "
                "'A condemned man with an appetite. Delicious. Deliver that Turnkey Ledger to me, and I will show you pleasures "
                "that make heaven look like a graveyard.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_start_quest_romance",
                    text="'Consider it delivered.'",
                    next_node="silve_quest_accepted",
                    quest_trigger="q_silk_cyanide",
                    quest_stage_set=1
                )
            ]
        ),
        "silve_quest_complete": DialogueNode(
            id="silve_quest_complete",
            speaker_name="Madame Silve",
            text=(
                "Silve turns the pages of the bloodstained Turnkey Ledger, her lips curling into a wicked smile. "
                "'Blackmail on every magistrate in the province. Exquisite.' She slides a forged Imperial Transit Pass into your coat pocket, "
                "her hand lingering provocatively against your inner thigh, her perfume overpowering the sulfur outside."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_intimacy_action",
                    text="Pull her into your lap and claim your decadent reward behind the velvet drapes.",
                    next_node="silve_intimacy_scene",
                    is_intimacy_action=True,
                    relationship_change=25
                ),
                DialogueChoice(
                    id="c_silve_leave_business",
                    text="'My thanks for the pass, Madame. I must make for the gate.'",
                    next_node="silve_farewell",
                    relationship_change=10
                )
            ]
        ),

        # --- Madame Silve 10-Step Erotic Sequence: The Gilded Rat (Default Scene) ---
        # Step 1: Initiating (Private Boudoir & Disrobing)
        "silve_intimacy_scene": DialogueNode(
            id="silve_intimacy_scene",
            speaker_name="Madame Silve",
            text=(
                "Silve guides you past heavy midnight-velvet curtains into her private sanctuary. Scented candles illuminate opulent crimson divans "
                "and piles of goose-down pillows. The sweet aroma of opium and spiced plum wine fills the air. "
                "With practiced, intoxicating grace, Silve unties her bodice strings. The tight black velvet opens, exposing her voluptuous, creamy bosom "
                "and narrow waist to your gaze. She laughs huskily, sliding her manicured fingers down your chest. "
                "'You fought like a demon for my ledger, wanderer. Tonight, I will show you what a true courtesan does with an iron-hearted survivor.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step2",
                    text="Embrace her against the cushions and taste the spiced wine on her lips.",
                    next_node="silve_gilded_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                ),
                # Alias for existing test
                DialogueChoice(
                    id="c_silve_eroge_boudoir",
                    text="Embrace her against the cushions and taste the spiced wine on her lips.",
                    next_node="silve_gilded_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        "silve_gilded_step1_initiate": DialogueNode(
            id="silve_gilded_step1_initiate",
            speaker_name="Madame Silve",
            text=(
                "Silve guides you past heavy midnight-velvet curtains into her private sanctuary. Scented candles illuminate opulent crimson divans "
                "and piles of goose-down pillows. The sweet aroma of opium and spiced plum wine fills the air. "
                "With practiced, intoxicating grace, Silve unties her bodice strings. The tight black velvet opens, exposing her voluptuous, creamy bosom "
                "and narrow waist to your gaze. She laughs huskily, sliding her manicured fingers down your chest. "
                "'You fought like a demon for my ledger, wanderer. Tonight, I will show you what a true courtesan does with an iron-hearted survivor.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_step1_choice",
                    text="Embrace her against the cushions and taste the spiced wine on her lips.",
                    next_node="silve_gilded_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        # Step 2: Foreplay & Branching Choices
        "silve_gilded_step2_foreplay": DialogueNode(
            id="silve_gilded_step2_foreplay",
            speaker_name="Madame Silve",
            text=(
                "Silve pulls you onto the velvet mattress, straddling your lap with a breathless purr. Her bare breasts, full, alabaster, and warm, "
                "brush against your chest as she unfastens your trousers with hungry, practiced fingers. "
                "'No politics tonight, wanderer,' she whispers against your ear, her teeth gently tugging your earlobe while her hips grind slowly into your hardening length. "
                "'Only skin, sweat, and fire. Show me what life feels like before the inquisitors turn this city to glass.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_branch_sensual",
                    text="[Courtesan Worship] Roll her onto her back, fondling her bare curves and kissing down her heaving cleavage.",
                    next_node="silve_gilded_step3_sensual",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_gilded_branch_oral",
                    text="[Devoted Oral Ecstasy] Burrow between her soft, perfumed thighs for lavish oral worship.",
                    next_node="silve_gilded_step3_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_gilded_branch_wine",
                    text="[Spiced Wine Tease] Pour dark spiced plum wine across her cleavage and lick it clean from her skin.",
                    next_node="silve_gilded_step3_wine",
                    is_intimacy_action=True
                ),
                # Aliases for compatibility
                DialogueChoice(
                    id="c_silve_eroge_take_control",
                    text="Roll her onto her back, spreading her soft legs and sliding inside her slick depths.",
                    next_node="silve_gilded_step3_sensual",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_oral",
                    text="Burrow between her soft, perfumed thighs and lavish her swollen core with devoted oral worship.",
                    next_node="silve_gilded_step3_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_wine",
                    text="Pour dark spiced plum wine across her cleavage and lick it from her skin before claiming her.",
                    next_node="silve_gilded_step3_wine",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_eroge_boudoir": DialogueNode(
            id="silve_eroge_boudoir",
            speaker_name="Madame Silve",
            text=(
                "Silve pulls you onto the velvet mattress, straddling your lap with a breathless purr. Her bare breasts, full, alabaster, and warm, "
                "brush against your chest as she unfastens your trousers with hungry, practiced fingers. "
                "'No politics tonight, wanderer,' she whispers against your ear, her teeth gently tugging your earlobe while her hips grind slowly into your hardening length. "
                "'Only skin, sweat, and fire. Show me what life feels like before the inquisitors turn this city to glass.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_take_control_alias",
                    text="Roll her onto her back, spreading her soft legs and sliding inside her slick depths.",
                    next_node="silve_gilded_step3_sensual",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_oral_alias",
                    text="Burrow between her soft, perfumed thighs and lavish her swollen core with devoted oral worship.",
                    next_node="silve_gilded_step3_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_wine_alias",
                    text="Pour dark spiced plum wine across her cleavage and lick it from her skin before claiming her.",
                    next_node="silve_gilded_step3_wine",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 3: Deepening Foreplay (Branch Outcomes)
        "silve_gilded_step3_sensual": DialogueNode(
            id="silve_gilded_step3_sensual",
            speaker_name="Madame Silve",
            text=(
                "Rolling her onto the disheveled silk sheets, your hands explore her ample curves, fondling the ripe weight of her breasts "
                "while your thumbs gently roll her erect, dark-pink nipples. Silve gasps softly, arching her back off the bed with sultry pleasure. "
                "Her hips roll instinctively upward against your thighs, her breath hot and spiced with cloves against your neck. "
                "'You have wonderful hands, wanderer... strong, greedy, and unhurried.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_sensual_to_step4",
                    text="Slide your palm down her silky stomach toward her soaked lace breeches.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_gilded_step3_oral": DialogueNode(
            id="silve_gilded_step3_oral",
            speaker_name="Madame Silve",
            text=(
                "Burrowing between her soft, perfumed thighs, your hands grasp her curved buttocks, lifting her into the candlelight. "
                "Her intimate folds are drenched with arousal, glistening and swollen with need. When your tongue laps up the length of her slit and suckles her clitoris, "
                "Silve cries out in wanton abandon, her elegant composure completely disintegrating into desperate, ragged gasps. "
                "Her manicured nails tangle tightly in your hair, her pelvis bucking greedily against your face. 'Mmm... ah! God, you wicked man... your tongue is pure sin!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_oral_to_step4",
                    text="Caress her glistening cleft and prepare her body for deep penetration.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_enter_from_oral",
                    text="Rise up, spread her velvet-soft thighs wide, and bury your length to the hilt within her.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_eroge_foreplay_oral": DialogueNode(
            id="silve_eroge_foreplay_oral",
            speaker_name="Madame Silve",
            text=(
                "Burrowing between her soft, perfumed thighs, your hands grasp her curved buttocks, lifting her into the candlelight. "
                "Her intimate folds are drenched with arousal, glistening and swollen with need. When your tongue laps up the length of her slit and suckles her clitoris, "
                "Silve cries out in wanton abandon, her elegant composure completely disintegrating into desperate, ragged gasps. "
                "Her manicured nails tangle tightly in your hair, her pelvis bucking greedily against your face. 'Mmm... ah! God, you wicked man... your tongue is pure sin!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_enter_from_oral_fwd",
                    text="Rise up, spread her velvet-soft thighs wide, and bury your length to the hilt within her.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_gilded_step3_wine": DialogueNode(
            id="silve_gilded_step3_wine",
            speaker_name="Madame Silve",
            text=(
                "You uncork a crystal flask of dark, spiced plum wine, pouring a warm ruby stream down her pale throat and into the valley between her heavy breasts. "
                "Your mouth follows the intoxicating trail, licking the spiced vintage from her skin while suckling her taut, wine-stained nipples. "
                "Silve writhes beneath you, moaning your name in sheer sensory delirium as her hands claw at your shoulders. "
                "'You ravishing devil... take me now! Don't make me wait another second!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_wine_to_step4",
                    text="Trace your wet lips down to her navel and slip your hand between her thighs.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_eroge_enter_from_wine",
                    text="Push into her drenched center with commanding rhythm to share the explosive finish.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_eroge_foreplay_wine": DialogueNode(
            id="silve_eroge_foreplay_wine",
            speaker_name="Madame Silve",
            text=(
                "You uncork a crystal flask of dark, spiced plum wine, pouring a warm ruby stream down her pale throat and into the valley between her heavy breasts. "
                "Your mouth follows the intoxicating trail, licking the spiced vintage from her skin while suckling her taut, wine-stained nipples. "
                "Silve writhes beneath you, moaning your name in sheer sensory delirium as her hands claw at your shoulders. "
                "'You ravishing devil... take me now! Don't make me wait another second!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_enter_from_wine_fwd",
                    text="Push into her drenched center with commanding rhythm to share the explosive finish.",
                    next_node="silve_gilded_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 4: Intimate Caresses & Lubrication
        "silve_gilded_step4_caress": DialogueNode(
            id="silve_gilded_step4_caress",
            speaker_name="Madame Silve",
            text=(
                "Pushing aside her gossamer silk undergarments, your fingers delve into her dripping cleft. "
                "Silve is scorching hot, drenched with honeyed lubrication that slicks your fingers with every caress. "
                "Her hips buck up in rhythm with your stroking, a husky purr escaping her lips as she reaches down to stroke your rigid erection. "
                "'Feel how badly I want you, darling... you've completely conquered the madam of Oakhaven. Take your prize.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step5",
                    text="Align your throbbing shaft with her soaking entrance and push inside.",
                    next_node="silve_gilded_step5_entry",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 5: Penetration & Full Sheathing
        "silve_gilded_step5_entry": DialogueNode(
            id="silve_gilded_step5_entry",
            speaker_name="Madame Silve",
            text=(
                "Parting her creamy thighs wide, you guide your swollen head into her dripping aperture. "
                "With a deliberate, unyielding press of your hips, you breach her tight, velvety corridor. "
                "Silve lets out a loud, shuddering cry of pure gratification, her arms winding around your neck as she takes your full length into her core. "
                "Her snug walls hug you like a glove of living silk, the heat inside her almost unbearable in its intensity."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step6",
                    text="Let the initial wave of pleasure wash over both of you before moving.",
                    next_node="silve_gilded_step6_rhythm",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 6: Sinuous Cadence & Decadent Friction
        "silve_gilded_step6_rhythm": DialogueNode(
            id="silve_gilded_step6_rhythm",
            speaker_name="Madame Silve",
            text=(
                "Establishing a deep, sensual rhythm, you begin to stroke within her tight depths. "
                "Silve's hips roll against yours in perfect, decadent harmony, matching each thrust with seductive expertise. "
                "The friction between your bodies is intoxicating; sweat slicks both your chests as the rhythm turns wet, steady, and hypnotic. "
                "Her breathless murmurs of praise and sultry laughter fill the candlelit boudoir."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step7",
                    text="Lock her shapely legs around your waist to drive into her deepest core.",
                    next_node="silve_gilded_step7_shift",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 7: Positional Shift & Escalation
        "silve_gilded_step7_shift": DialogueNode(
            id="silve_gilded_step7_shift",
            speaker_name="Madame Silve",
            text=(
                "Hoisting her hips higher upon the cushions, you lock her slender legs around your waist. "
                "The new angle permits devastatingly deep penetration; every thrust buries you to the absolute hilt, bottoming out against her cervix. "
                "Loud, wet slaps echo off the velvet canopy. Silve's worldly poise shatters into wanton gasps, her fingernails biting deep into your back."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step8",
                    text="Accelerate your thrusts into a commanding, relentless tempo.",
                    next_node="silve_gilded_step8_frenzy",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 8: Fierce Cadence & Vocal Surrender
        "silve_gilded_step8_frenzy": DialogueNode(
            id="silve_gilded_step8_frenzy",
            speaker_name="Madame Silve",
            text=(
                "The pace turns frantic, urgent, and wild. You hammer into her with primal ferocity, driving the breath from her lungs with every impact. "
                "Silve throws her head back into the pillows, her voluptuous breasts bouncing with every violent stroke, "
                "her moans rising into ragged, breathless cries of ecstasy. 'Ah... yes! Give it to me, wanderer... don't you dare stop!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step9",
                    text="Drive through the rising heat as her inner walls begin to seize.",
                    next_node="silve_gilded_step9_precipice",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 9: The Precipice / Edging
        "silve_gilded_step9_precipice": DialogueNode(
            id="silve_gilded_step9_precipice",
            speaker_name="Madame Silve",
            text=(
                "The peak rushes upon both of you like a fevered wildfire. Silve's internal passage begins to convulse violently, "
                "suctioning and clutching your shaft with frantic, desperate contractions. "
                "Her eyes roll back in sheer sensory delirium, her hips bucking up against yours to pull you as deep as humanly possible. "
                "'I'm breaking... darling, I'm coming! Fill me... pour it all inside!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_step10",
                    text="Deliver one final, all-consuming plunge and surrender to the climax.",
                    next_node="silve_gilded_step10_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 10: Explosive Climax
        "silve_gilded_step10_climax": DialogueNode(
            id="silve_gilded_step10_climax",
            speaker_name="Madame Silve",
            text=(
                "With a final, devastating thrust, you bury your length to the absolute root. "
                "Silve's body arches rigidly off the mattress as an earth-shattering orgasm rips through her, her inner walls convulsing in wild, unending spasms around your shaft. "
                "With a guttural roar, you spill copious waves of boiling release deep inside her trembling womb, flooding her core as you collapse together into the disheveled crimson silks in spent, breathless ecstasy."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_gilded_to_afterglow",
                    text="Recline together on the cushions in decadent afterglow.",
                    next_node="silve_gilded_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Silve's Scented Silk Favor"
                ),
                # Alias for existing test
                DialogueChoice(
                    id="c_silve_eroge_afterglow",
                    text="Recline together on the cushions in decadent afterglow.",
                    next_node="silve_gilded_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Silve's Scented Silk Favor"
                )
            ]
        ),
        "silve_eroge_climax": DialogueNode(
            id="silve_eroge_climax",
            speaker_name="Madame Silve",
            text=(
                "With a final, devastating thrust, you bury your length to the absolute root. "
                "Silve's body arches rigidly off the mattress as an earth-shattering orgasm rips through her, her inner walls convulsing in wild, unending spasms around your shaft. "
                "With a guttural roar, you spill copious waves of boiling release deep inside her trembling womb, flooding her core as you collapse together into the disheveled crimson silks in spent, breathless ecstasy."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_afterglow_alias",
                    text="Recline together on the cushions in decadent afterglow.",
                    next_node="silve_gilded_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Silve's Scented Silk Favor"
                )
            ]
        ),
        # Afterglow & Bonding (Gilded Rat)
        "silve_gilded_afterglow": DialogueNode(
            id="silve_gilded_afterglow",
            speaker_name="Madame Silve",
            text=(
                "Silve lounges across your chest, tracing your jawline with a satisfied, contented smile. The dread of the approaching purge has vanished, "
                "replaced by pure intimacy and dark devotion. She presses a perfumed, embroidered black silk handkerchief into your hand, "
                "along with a pouch of 35 Sovereigns. 'This silk bears my crest and secret scent, handsome. Any fence, guard, or merchant in the province "
                "will give you a 25% discount and heed your word. Survive tonight, wanderer... and come back to my bed.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_recruit_afterglow",
                    text="'The city is doomed to burn at midnight, Silve. Take your poisoned stiletto and come with me. Join my party.'",
                    next_node="silve_recruited",
                    relationship_change=20
                ),
                DialogueChoice(
                    id="c_silve_companion_return_hub",
                    text="Resume traveling together.",
                    next_node="silve_companion_hub"
                ),
                DialogueChoice(
                    id="c_silve_afterglow_farewell",
                    text="'I will return, Silve. Now I must reach the gate.'",
                    next_node="silve_farewell"
                )
            ]
        ),
        "silve_eroge_afterglow": DialogueNode(
            id="silve_eroge_afterglow",
            speaker_name="Madame Silve",
            text=(
                "Silve lounges across your chest, tracing your jawline with a satisfied, contented smile. The dread of the approaching purge has vanished, "
                "replaced by pure intimacy and dark devotion. She presses a perfumed, embroidered black silk handkerchief into your hand, "
                "along with a pouch of 35 Sovereigns. 'This silk bears my crest and secret scent, handsome. Any fence, guard, or merchant in the province "
                "will give you a 25% discount and heed your word. Survive tonight, wanderer... and come back to my bed.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_recruit_afterglow_alias",
                    text="'The city is doomed to burn at midnight, Silve. Take your poisoned stiletto and come with me. Join my party.'",
                    next_node="silve_recruited",
                    relationship_change=20
                ),
                DialogueChoice(
                    id="c_silve_companion_return_hub_alias",
                    text="Resume traveling together.",
                    next_node="silve_companion_hub"
                ),
                DialogueChoice(
                    id="c_silve_afterglow_farewell_alias",
                    text="'I will return, Silve. Now I must reach the gate.'",
                    next_node="silve_farewell"
                )
            ]
        ),
        "silve_recruited": DialogueNode(
            id="silve_recruited",
            speaker_name="Madame Silve",
            text=(
                "Silve fastens a dark traveling cloak of oiled velvet, concealing her poison-tipped stiletto and alchemical vials within tailored sheaths. "
                "Her lips curve into a wicked, seductive smirk. 'A rogue and her marked wanderer defying the Grand Inquisitor's pyre? "
                "How deliciously scandalous. Lead on, darling—I'm yours.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_recruited_to_hub",
                    text="'Let us move together, Silve. Stay in my shadow.'",
                    next_node="silve_companion_hub"
                )
            ]
        ),
        # --- Madame Silve Companion Party Dialogue Hub & Interactions ---
        "silve_companion_hub": DialogueNode(
            id="silve_companion_hub",
            speaker_name="Madame Silve",
            text=(
                "Silve glides through the alley gloom alongside you, her dark silk cloak trailing like smoke across the damp cobbles. "
                "A subtle scent of jasmine, crushed cloves, and opium precedes her, masking the rot of the quarantine. "
                "She toys with a poison-tipped stiletto with practiced flair before sheathing it into her corset. "
                "'Still alive and still dangerous, handsome?' she murmurs with a sly, knowing smile. 'I find myself enjoying our little partnership immensely.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_companion_talk",
                    text="Converse with Silve about her spy network and secret escape intelligence.",
                    next_node="silve_companion_talk"
                ),
                DialogueChoice(
                    id="c_silve_companion_intimacy",
                    text="[Erotic Scene] Draw Silve into a curtained alcove for an intoxicating carnal encounter.",
                    next_node="silve_companion_intimacy_start",
                    is_intimacy_action=True,
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_silve_companion_contraband",
                    text="Ask Silve for contraband supplies or pocket change (Contraband Check).",
                    next_node="silve_companion_contraband"
                ),
                DialogueChoice(
                    id="c_silve_companion_dismiss",
                    text="'Silve, slip back to the Gilded Rat. I must proceed alone for now.'",
                    next_node="silve_companion_dismiss"
                )
            ]
        ),
        "silve_companion_talk": DialogueNode(
            id="silve_companion_talk",
            speaker_name="Madame Silve",
            text=(
                "Silve leans close against your arm, her eyes scanning the silhouettes of the ruined tenements. "
                "'Information is the only true currency that outlasts kingdoms, darling. But having a warrior who can turn iron into survival? "
                "That is a rare luxury. When we break out of this burning trap, the entire outer province will be ours for the taking.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_comp_talk_intimacy",
                    text="Wrap an arm around her waist. 'Then let us take our reward right here, Silve.'",
                    next_node="silve_companion_intimacy_start",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_comp_talk_return",
                    text="'Keep your eyes open, Silve. Let's move.'",
                    next_node="silve_companion_hub"
                )
            ]
        ),
        "silve_companion_intimacy_start": DialogueNode(
            id="silve_companion_intimacy_start",
            speaker_name="Madame Silve",
            text=(
                "Pulling Silve into a secluded, curtained recess away from prying eyes, you seal off the toxic smog of Oakhaven. "
                "Her manicured hands immediately glide onto your chest, unbuttoning your tunic with hungry dexterity. "
                "'Always so urgent, darling... and so beautifully relentless,' she purrs huskily, shrugging her heavy velvet mantle to the floor to reveal her laced corset and creamy, heaving bosom. "
                "'Show me what an iron-willed wanderer does when he claims his courtesan.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_comp_to_location_scene",
                    text="Pull her into your arms and surrender to carnal desire.",
                    next_node="silve_gilded_step1_initiate",
                    is_intimacy_action=True
                ),
                # Aliases for compatibility
                DialogueChoice(
                    id="c_silve_companion_oral",
                    text="Drop to your knees, untying her silken breeches to worship her dripping heat.",
                    next_node="silve_companion_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_companion_coupling_direct",
                    text="Turn her against the velvet cushions and drive deeply into her wet depths.",
                    next_node="silve_companion_coupling",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_companion_oral": DialogueNode(
            id="silve_companion_oral",
            speaker_name="Madame Silve",
            text=(
                "Parting her gossamer lace undergarments, you discover her swollen feminine folds thoroughly drenched and burning with arousal. "
                "When your tongue licks up the length of her slit and seals over her sensitive clitoris, Silve gasps sharply, her cultured composure shattering into wanton abandon. "
                "Her manicured nails press into your shoulders as she tilts her pelvis greedily against your mouth. "
                "'Mmm... ah! God, you wicked man... your mouth is pure sin!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_companion_to_coupling",
                    text="Rise up and sheath yourself into her tight, welcoming core.",
                    next_node="silve_companion_coupling",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_companion_coupling": DialogueNode(
            id="silve_companion_coupling",
            speaker_name="Madame Silve",
            text=(
                "Pulling her hips flush against yours, you drive your hardened shaft deep into her tight, velvety warmth. Silve lets out a loud, shuddering moan of sheer gratification, her arms circling your neck as she meets every thrust with sinuous, rolling hip motions. "
                "Her tight passage grasps your length like a hot glove, the friction between your bodies slick and urgent. Each powerful stroke elicits breathless whimpers and sultry praise from her lips as she yields completely to your dominant cadence."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_companion_to_climax",
                    text="Pound into her sweet depths with commanding ferocity to reach the climax.",
                    next_node="silve_companion_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_companion_climax": DialogueNode(
            id="silve_companion_climax",
            speaker_name="Madame Silve",
            text=(
                "Locking her legs around your waist, you drive home with fierce, breathless intensity. Silve's body arches off the velvet divan as an earth-shattering orgasm rips through her, her inner walls convulsing in wild, uncontrollable ripples around your shaft. "
                "With a guttural growl, you bury your length to the absolute hilt, flooding her deep within with hot, pulsing release. "
                "She shivers in your embrace, panting heavily against your lips as your release fills her completely, banishing every shred of despair from your mind."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_companion_afterglow",
                    text="Linger together in the intoxicating warmth of the afterglow.",
                    next_node="silve_companion_afterglow",
                    is_intimacy_action=True,
                    relationship_change=20
                )
            ]
        ),
        "silve_companion_afterglow": DialogueNode(
            id="silve_companion_afterglow",
            speaker_name="Madame Silve",
            text=(
                "Silve reclines against your chest with a decadent, purring laugh, trailing her fingers along your jawline. "
                "'You truly know how to spoil a woman, wanderer. With steel like yours at my side, let the inquisitors try to stop us.' (Dread purged to 0. Devotion absolute)."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_companion_return_hub",
                    text="Resume traveling together.",
                    next_node="silve_companion_hub"
                )
            ]
        ),

        # --- Madame Silve 10-Step Erotic Sequence: The Ruined Chantry (Location Unique Scene) ---
        # Step 1: Initiating in the Desecrated Sanctuary
        "silve_chantry_step1_initiate": DialogueNode(
            id="silve_chantry_step1_initiate",
            speaker_name="Madame Silve",
            text=(
                "Leading Silve through the shadowed nave of Saint Marrow into the desecrated sanctuary behind the altar screen, "
                "moonlight filters through broken stained glass, illuminating kneeling statues of ancient martyrs. "
                "Silve lets out a low, wicked chuckle as she lets her dark velvet mantle slip onto the consecrated stone steps. "
                "'Making love on the altar of saints while the inquisitors prepare our pyre?' she purrs with an arch of her eyebrow, "
                "her manicured hands unfastening the clasps of her leather corset. 'You have a delightfully corrupt soul, wanderer. "
                "Let us see if the martyrs blush when you claim me here in their holy dark.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step2",
                    text="Help her shed her bodice, exposing her alabaster curves against the cool stone.",
                    next_node="silve_chantry_step2_foreplay",
                    is_intimacy_action=True,
                    relationship_change=15
                )
            ]
        ),
        # Step 2: Foreplay & Branching Choices (Ruined Chantry)
        "silve_chantry_step2_foreplay": DialogueNode(
            id="silve_chantry_step2_foreplay",
            speaker_name="Madame Silve",
            text=(
                "Her corset parts, freeing her heavy, alabaster breasts in the silver moonlight. "
                "The chill of the chantry stones provides a delicious contrast against the burning heat radiating from her skin. "
                "Silve leans back against the marble altar railing, her lips parted with a sensual, mocking smirk that dares you to conquer her."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_branch_kiss",
                    text="[Altar Passion] Lift her onto the marble railing, kissing her mouth deeply while teasing her taut nipples.",
                    next_node="silve_chantry_step3_kiss",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_chantry_branch_oral",
                    text="[Sacrilegious Devotion] Kneel upon the velvet prayer cushion and worship her glistening cleft with your tongue.",
                    next_node="silve_chantry_step3_oral",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_chantry_branch_dominant",
                    text="[Commanding Dominion] Turn her facing the stone altar, lifting her silk skirts to claim her from behind.",
                    next_node="silve_chantry_step3_dominant",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 3: Deepening Foreplay (Branch Outcomes)
        "silve_chantry_step3_kiss": DialogueNode(
            id="silve_chantry_step3_kiss",
            speaker_name="Madame Silve",
            text=(
                "Lifting her bodily onto the polished marble communion rail, you capture her lips in a deep, ravenous kiss. "
                "Your hands cup her full, creamy breasts, squeezing their lush weight while your thumbs circle her sensitive, wine-hued nipples. "
                "Silve lets out a breathless, wanton moan that reverberates softly in the vaulted chantry ceiling, her manicured nails digging into your biceps."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_kiss_to_step4",
                    text="Slide your hand beneath her skirts, tracing the humid heat of her inner thighs.",
                    next_node="silve_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_chantry_step3_oral": DialogueNode(
            id="silve_chantry_step3_oral",
            speaker_name="Madame Silve",
            text=(
                "Dropping to your knees onto the worn velvet prayer cushion, you spread her smooth, stockinged thighs wide in the moonlit gloom. "
                "Her feminine folds are already drenched with slippery nectar, glowing faintly in the silver light. "
                "When your mouth covers her swollen clitoris, suckling and lapping with fervent devotion, Silve gasps in breathless ecstasy. "
                "Her hands clutch your hair, tilting her hips down against your face as her knees tremble violently. 'Ah... god! What a wicked, blasphemous tongue!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_oral_to_step4",
                    text="Rise up and slide your wet fingers through her soaking core.",
                    next_node="silve_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_chantry_step3_dominant": DialogueNode(
            id="silve_chantry_step3_dominant",
            speaker_name="Madame Silve",
            text=(
                "Spinning her around, you press her chest flat against the cold marble slab of the altar. "
                "Bunching her black silk skirts up around her hips, you grasp her rounded buttocks, kneading the soft flesh firmly. "
                "Silve lets out an appreciative, wanton purr, glancing back over her shoulder with smoldering eyes. "
                "'Treat me like a conqueror claims his spoils, wanderer. I want to feel the raw iron in you.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_dom_to_step4",
                    text="Part her dripping folds with your fingers and prepare her for your entrance.",
                    next_node="silve_chantry_step4_caress",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 4: Intimate Caresses & Sacred Lubrication
        "silve_chantry_step4_caress": DialogueNode(
            id="silve_chantry_step4_caress",
            speaker_name="Madame Silve",
            text=(
                "Your fingers probe the weeping depths of her passage, testing her heat against the cold, echoing stillness of the cathedral. "
                "Silve's inner walls grip your fingers with urgent, hot suction, completely soaked with sweet lubrication. "
                "She shivers in your grasp, her breath hitching in ragged gasps. 'Enough foreplay... pierce me with that magnificent blade of yours!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step5",
                    text="Align your throbbing shaft with her dripping slit and breach her warmth.",
                    next_node="silve_chantry_step5_entry",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 5: Penetration in the Moonlit Sanctuary
        "silve_chantry_step5_entry": DialogueNode(
            id="silve_chantry_step5_entry",
            speaker_name="Madame Silve",
            text=(
                "With a deliberate, unyielding forward drive of your hips, you sink your rigid head into her tight aperture. "
                "Silve's breath catches in her throat with a sharp cry of pleasure as her snug walls part and stretch to receive your full girth. "
                "You push smoothly until your hips meet hers with a wet, resonant thud against the altar steps. "
                "She throws her head back, her throat pale and exposed in the moonlight, weeping soft tears of pure sensual fulfillment."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step6",
                    text="Pause to let her internal walls hug your shaft before beginning to move.",
                    next_node="silve_chantry_step6_rhythm",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 6: Resonant Cadence in the Nave
        "silve_chantry_step6_rhythm": DialogueNode(
            id="silve_chantry_step6_rhythm",
            speaker_name="Madame Silve",
            text=(
                "Drawing back almost to the tip, you plunge deeply back into her feverish core. "
                "Each slow, rhythmic thrust draws a melodic moan from Silve's lips that echoes off the cracked marble pillars. "
                "Her hips roll with seasoned grace, meeting your thrusts with practiced precision, her inner muscles clutching your shaft in waves of tight suction."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step7",
                    text="Hoist her higher onto the altar stone and deepen your strokes.",
                    next_node="silve_chantry_step7_shift",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 7: Positional Shift & Escalation
        "silve_chantry_step7_shift": DialogueNode(
            id="silve_chantry_step7_shift",
            speaker_name="Madame Silve",
            text=(
                "Lifting her legs onto your shoulders, you pin her beneath you upon the altar slab, driving into her at a steeper, devastating angle. "
                "Loud, wet slaps resound through the hollow sanctuary as your pelvis crashes against hers. "
                "Silve's worldly composure is wholly obliterated; she claws at the stone carvings, her breathless whimpers turning into wanton, uninhibited cries."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step8",
                    text="Drive the cadence into a fierce, relentless pounding.",
                    next_node="silve_chantry_step8_frenzy",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 8: Sacred Frenzy & Vocal Surrender
        "silve_chantry_step8_frenzy": DialogueNode(
            id="silve_chantry_step8_frenzy",
            speaker_name="Madame Silve",
            text=(
                "Your thrusts become rapid, heavy, and punishing. Sweat slicks your skin, dripping onto her heaving chest in the moonlit gloom. "
                "Silve wraps her arms around your neck, burying her face into your collarbone as she shamelessly babbles wanton endearments, "
                "urging you harder and deeper with desperate, hungry whispers. 'Take it all, darling... make this holy ground remember us!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step9",
                    text="Drive through the rising heat as her inner passage begins to convulse.",
                    next_node="silve_chantry_step9_precipice",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 9: The Edge of Absolution
        "silve_chantry_step9_precipice": DialogueNode(
            id="silve_chantry_step9_precipice",
            speaker_name="Madame Silve",
            text=(
                "The climax approaches like an unstoppable storm. Silve's internal passage begins to spasm in violent, rhythmic contractions, "
                "clutching your shaft with desperate, overwhelming suction. Her legs lock around your waist, her body coiling tight as a drawn bow. "
                "'I'm shattering... wanderer, oh gods, don't stop! Right there!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_step10",
                    text="Bury your length to the root and surrender to the explosive release.",
                    next_node="silve_chantry_step10_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        # Step 10: Climax at the Altar
        "silve_chantry_step10_climax": DialogueNode(
            id="silve_chantry_step10_climax",
            speaker_name="Madame Silve",
            text=(
                "With one final, thunderous plunge, you drive home to the absolute root. "
                "Silve screams softly into your neck as a transcendent, earth-shattering orgasm rips through her, her body convulsing in wild, unending ripples. "
                "With a guttural roar, you flood her deep within with boiling, pulsing seed, filling her core completely as both of you collapse across the altar slab in breathless, spent ecstasy."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_to_afterglow",
                    text="Hold each other in the peaceful, moonlit silence of the sanctuary.",
                    next_node="silve_chantry_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        # Afterglow (Ruined Chantry)
        "silve_chantry_afterglow": DialogueNode(
            id="silve_chantry_afterglow",
            speaker_name="Madame Silve",
            text=(
                "Resting together amidst her velvet cloak on the altar steps, Silve gently strokes your hair with a lazy, satisfied smile. "
                "'If this is sacrilege, darling, then let the heavens strike us down now,' she whispers huskily against your lips. "
                "'I have never felt so alive, nor so utterly claimed. When the gates open, we conquer the outer barrens together.' "
                "(All dread eradicated. Devotion absolute)."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_chantry_return_hub",
                    text="Collect your weapons and return to traveling together.",
                    next_node="silve_companion_hub"
                )
            ]
        ),
        "silve_companion_contraband": DialogueNode(
            id="silve_companion_contraband",
            speaker_name="Madame Silve",
            text=(
                "Silve winks slyly and reaches into a secret pocket of her velvet cloak, pulling out a sealed flask of Spiced Plum Wine (or extra Sovereigns if you already carry wine). "
                "'A little something to keep your heart warm and your steel sharp, darling.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_contraband_return",
                    text="'Much obliged, Silve. Let's keep moving.'",
                    next_node="silve_companion_hub"
                )
            ]
        ),
        "silve_companion_dismiss": DialogueNode(
            id="silve_companion_dismiss",
            speaker_name="Madame Silve",
            text=(
                "Silve arches an eyebrow and gives a coy, understanding pucker of her lips. "
                "'Getting secretive on me, handsome? Very well. I'll be waiting in my boudoir at the Gilded Rat. Don't keep me waiting too long.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_confirm_dismiss",
                    text="Watch her disappear into the velvet shadows of the Gilded Rat.",
                    next_node="silve_companion_dismiss_final"
                ),
                DialogueChoice(
                    id="c_silve_cancel_dismiss",
                    text="'On second thought, Silve, stay by my side.'",
                    next_node="silve_companion_hub"
                )
            ]
        ),
        "silve_companion_dismiss_final": DialogueNode(
            id="silve_companion_dismiss_final",
            speaker_name="Madame Silve",
            text="Madame Silve returns to the Gilded Rat Parlour.",
            choices=[]
        ),
        "silve_farewell": DialogueNode(
            id="silve_farewell",
            speaker_name="Madame Silve",
            text=(
                "'Run fast, handsome wanderer. May the shadows wrap around you like silk.'"
            ),
            choices=[]
        )
    }

    toby_dialogues = {
        "root": DialogueNode(
            id="root",
            speaker_name="Little Toby",
            text=(
                "A hollow-cheeked boy in oversized rags huddles beneath the gibbet platform, shivering uncontrollably. "
                "He clutches an iron key ring and a leather-bound book against his ribs, terrified of the zealot guards. "
                "'P-please... don't let them burn me mister! I didn't steal nothing, I swear!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_toby_comfort",
                    text="Kneel down, speaking softly. 'I won't hurt you, lad. Here, take some rations.'",
                    next_node="toby_comforted",
                    item_required="Charred Rations",
                    relationship_change=30,
                    faction_changes={"pariahs": 20}
                ),
                DialogueChoice(
                    id="c_toby_teach",
                    text="[Guile 11] 'Keep low in the ditch, Toby. If a guard turns his torch, stay still like a stone. Watch my footing.'",
                    next_node="toby_taught",
                    required_stat="guile",
                    required_value=11,
                    relationship_change=25
                ),
                DialogueChoice(
                    id="c_toby_intimidate",
                    text="[Sinew 12] 'Hand over that key and book right now, or I'll throw you to the Dawnbound.'",
                    next_node="toby_robbed",
                    required_stat="sinew",
                    required_value=12,
                    relationship_change=-40,
                    faction_changes={"pariahs": -25},
                    item_rewards=["Master Sluice Key", "Turnkey's Stolen Ledger"]
                )
            ]
        ),
        "toby_taught": DialogueNode(
            id="toby_taught",
            speaker_name="Little Toby",
            text=(
                "Toby's wide eyes soak in your movements. He mimics your crouching stride beneath the shadows of the scaffold. "
                "'You move like a ghost, mister! Here... take this Tarnished Iron Nail I found. You can bend it into a lockpick "
                "to open the high gibbet cages if you need to recover anything up there!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_toby_back_after_taught",
                    text="'Good lad. Now let's see about food.'",
                    next_node="root"
                )
            ]
        ),
        "toby_comforted": DialogueNode(
            id="toby_comforted",
            speaker_name="Little Toby",
            text=(
                "Toby ravenously devours the rations, tears spilling down his soot-stained face. 'Nobody gave me food since yesterday... "
                "You're a good man, mister. Take this—it's the Master Sluice Key! The turnkey dropped it when the sickness took him. "
                "It opens the iron gate in the Trench. And here's his book with all the city secrets!' He hands you both items."
            ),
            choices=[
                DialogueChoice(
                    id="c_toby_take_key",
                    text="Ruffle his hair gently. 'Hide in the hollow barrels until nightfall, Toby. Stay quiet and stay alive.'",
                    next_node="toby_saved",
                    item_rewards=["Master Sluice Key", "Turnkey's Stolen Ledger"],
                    relationship_change=20
                ),
                DialogueChoice(
                    id="c_toby_send_safehouse",
                    text="'Go to the Gilded Rat parlour. Tell Madame Silve I sent you to hide in her dry cellar.'",
                    next_node="toby_safehouse",
                    item_rewards=["Master Sluice Key", "Turnkey's Stolen Ledger"],
                    relationship_change=35
                )
            ]
        ),
        "toby_safehouse": DialogueNode(
            id="toby_safehouse",
            speaker_name="Little Toby",
            text=(
                "'The fancy lady's place? With real blankets?!' Toby hugs your leg with tears streaming down his grimy face. "
                "'Thank you, mister! Toby won't ever forget you!' He scurries like a mouse into the alley toward the Gilded Rat."
            ),
            choices=[]
        ),
        "toby_saved": DialogueNode(
            id="toby_saved",
            speaker_name="Little Toby",
            text=(
                "'Thank you, mister! Toby won't forget this!' The boy scrambles into the shadows of the drainage culvert."
            ),
            choices=[]
        ),
        "toby_robbed": DialogueNode(
            id="toby_robbed",
            speaker_name="Little Toby",
            text=(
                "Toby screams in terror, dropping the key and book in the mud before fleeing like a frightened rabbit into the dark. "
                "You picked up the Master Sluice Key and Turnkey Ledger, but the pariahs watching from the alleys curse your name."
            ),
            choices=[]
        )
    }

    return {
        "sister_vanya": NPC(
            id="sister_vanya",
            name="Sister Vanya",
            title="The Dawnbound Chirurgeon",
            gender="female",
            faction_id="dawnshroud",
            description="A raven-haired woman in a soiled white habit, eyes burning with tragic fervor and deep exhaustion.",
            stats=Stats(sinew=8, guile=10, lucidity=16),
            max_hp=28,
            current_hp=28,
            relationship=15,
            is_combatant=True,
            can_romance=True,
            dialogue_root="root",
            dialogue_nodes=vanya_dialogues,
            active_quest_id="q_mercy_hemlock",
            loot=["Silver Dawnshroud Seal", "Chirurgeon Scalpel", "Purified Bandage"]
        ),
        "commander_malakor": NPC(
            id="commander_malakor",
            name="Commander Malakor",
            title="Iron Drake Veteran",
            gender="male",
            faction_id="iron_drakes",
            description="A hulking sellsword covered in scarred plate armor, radiating brute violence and suppressed grief.",
            stats=Stats(sinew=17, guile=12, lucidity=8),
            max_hp=45,
            current_hp=45,
            relationship=10,
            is_combatant=True,
            can_romance=False, # Male companion: strictly warrior brotherhood, non-romanceable
            dialogue_root="root",
            dialogue_nodes=malakor_dialogues,
            active_quest_id="q_blood_brass",
            loot=["Draketooth Greatsword", "Wolfsbane Nectar", "Iron Drake Insignia"]
        ),
        "madame_silve": NPC(
            id="madame_silve",
            name="Madame Silve",
            title="Mistress of the Gilded Rat",
            gender="female",
            faction_id="pariahs",
            description="A lavishly dressed secret broker draped in black velvet and sheer lace, smelling of opium and spices.",
            stats=Stats(sinew=9, guile=16, lucidity=14),
            max_hp=25,
            current_hp=25,
            relationship=15,
            is_combatant=True,
            can_romance=True,
            dialogue_root="root",
            dialogue_nodes=silve_dialogues,
            active_quest_id="q_silk_cyanide",
            loot=["Imperial Transit Pass", "Poison-Tipped Stiletto", "Velvet Coin Purse"]
        ),
        "little_toby": NPC(
            id="little_toby",
            name="Little Toby",
            title="Trench Scavenger Orphan",
            gender="male",
            faction_id="pariahs",
            description="A starving, dirt-caked orphan clenching a turnkey's ledger and a heavy brass ring.",
            stats=Stats(sinew=4, guile=14, lucidity=9),
            max_hp=15,
            current_hp=15,
            relationship=0,
            is_combatant=False,
            can_romance=False,
            dialogue_root="root",
            dialogue_nodes=toby_dialogues,
            loot=["Turnkey's Stolen Ledger"]
        )
    }

def get_prologue_quests() -> Dict[str, Quest]:
    return {
        "q_mercy_hemlock": Quest(
            id="q_mercy_hemlock",
            title="The Mercy of Hemlock",
            description="Sister Vanya needs Wolfsbane Nectar to mercifully end the suffering of her dying patients before the Dawnbound burns them alive.",
            giver_npc_id="sister_vanya",
            faction_id="dawnshroud",
            stages={
                1: QuestStage(
                    stage_id=1,
                    description="Acquire Wolfsbane Nectar from Commander Malakor at the Iron Drake Bastion.",
                    target_location="iron_bastion",
                    target_npc="commander_malakor"
                ),
                2: QuestStage(
                    stage_id=2,
                    description="Deliver the Wolfsbane Nectar to Sister Vanya in the Ruined Chantry.",
                    target_location="ruined_chantry",
                    target_npc="sister_vanya",
                    required_item="Wolfsbane Nectar"
                )
            },
            reward_items=["Silver Dawnshroud Seal"],
            reward_sovereigns=15,
            reward_relation=30,
            reward_faction_points=25,
            completion_text="Sister Vanya administers the nectar with tears in her eyes. The patients pass peacefully in their sleep before the fire falls."
        ),
        "q_blood_brass": Quest(
            id="q_blood_brass",
            title="Blood and Brass",
            description="Commander Malakor seeks his fallen brother Loras's Iron Signet ring from the corpse pyres in Gallow-Square.",
            giver_npc_id="commander_malakor",
            faction_id="iron_drakes",
            stages={
                1: QuestStage(
                    stage_id=1,
                    description="Search the charnel urns in the Gallow-Square for Loras's Iron Signet.",
                    target_location="gallow_square"
                ),
                2: QuestStage(
                    stage_id=2,
                    description="Return the signet to Commander Malakor at the Iron Drake Bastion.",
                    target_location="iron_bastion",
                    target_npc="commander_malakor",
                    required_item="Loras's Iron Signet"
                )
            },
            reward_items=["Wolfsbane Nectar"],
            reward_sovereigns=30,
            reward_relation=35,
            reward_faction_points=30,
            completion_text="Malakor clasps his brother's signet against his forehead in solemn silence. His loyalty to you is sealed."
        ),
        "q_silk_cyanide": Quest(
            id="q_silk_cyanide",
            title="Silk and Cyanide",
            description="Madame Silve requires the Turnkey's Stolen Ledger held by Little Toby in the Gallow-Square.",
            giver_npc_id="madame_silve",
            faction_id="pariahs",
            stages={
                1: QuestStage(
                    stage_id=1,
                    description="Obtain the Turnkey's Stolen Ledger from Little Toby in the Gallow-Square.",
                    target_location="gallow_square",
                    target_npc="little_toby"
                ),
                2: QuestStage(
                    stage_id=2,
                    description="Deliver the ledger to Madame Silve at the Gilded Rat Parlour.",
                    target_location="gilded_rat",
                    target_npc="madame_silve",
                    required_item="Turnkey's Stolen Ledger"
                )
            },
            reward_items=["Imperial Transit Pass"],
            reward_sovereigns=45,
            reward_relation=30,
            reward_faction_points=30,
            completion_text="Madame Silve locks the incriminating magistrate records in her iron chest, rewarding you with forged passage."
        )
    }

def get_prologue_factions() -> Dict[str, Dict[str, str]]:
    return {
        "dawnshroud": {
            "name": "Order of the Dawnshroud",
            "desc": "Zealot inquisitors who cleanse infection and sin with white phosphorus and brimstone.",
            "color": "#c4a052"
        },
        "iron_drakes": {
            "name": "The Iron Drakes",
            "desc": "Mercenary syndicate ruling the trade of blood, weapons, and extortion.",
            "color": "#8b0000"
        },
        "pariahs": {
            "name": "Pariahs of the Trench",
            "desc": "Outcasts, beggars, courtesans, and lepers surviving in the muck beneath the city.",
            "color": "#4a6b5d"
        }
    }
