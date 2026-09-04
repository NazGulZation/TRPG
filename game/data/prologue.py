"""Prologue chapter data: 'Ashen Solstice - The Sinking of Oakhaven'."""

from typing import Dict
from game.models import Stats, NPC, Location, Quest, QuestStage, DialogueNode, DialogueChoice

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

        # --- Eroge Spicy Multi-Stage Intimacy Sequence: Sister Vanya ---
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
                    id="c_vanya_eroge_unveil",
                    text="Reach for the lacings of her habit, gently stripping away her sacred vows.",
                    next_node="vanya_eroge_unveil",
                    is_intimacy_action=True,
                    relationship_change=15
                ),
                DialogueChoice(
                    id="c_vanya_minigame_start",
                    text="Engage in the 'Sanctum of the Flesh' Intimacy Minigame.",
                    next_node="vanya_eroge_minigame_start",
                    is_intimacy_action=True,
                    relationship_change=20
                )
            ]
        ),
        "vanya_eroge_minigame_start": DialogueNode(
            id="vanya_eroge_minigame_start",
            speaker_name="Sister Vanya",
            text=(
                "You lay Vanya onto the soft silk altar vestments. Her habit falls open, revealing high, flushed breasts crowned with rosy, sensitive nipples "
                "that harden in the cool crypt air. Her thighs tremble slightly with anticipation as she gazes up at you with parted lips. "
                "(The Intimacy Minigame has begun! Build her Arousal to 100% using tactile caresses, passionate rhythm, and whispered adoration)."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_mg_guile",
                    text="[Guile] Erogenous Caress: Trace your fingertips across her ribs, inner thighs, and sensitive cleft.",
                    next_node="vanya_mg_guile_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_mg_sinew",
                    text="[Sinew] Passionate Intensity: Pull her hips firmly against yours, kissing her throat with deep hunger.",
                    next_node="vanya_mg_sinew_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_mg_lucidity",
                    text="[Lucidity] Whispered Worship: Read her ragged breathing and whisper absolution while stroking her wet heat.",
                    next_node="vanya_mg_lucidity_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_mg_oral",
                    text="Devoted Oral Worship: Part her trembling thighs and press your lips directly to her glistening core.",
                    next_node="vanya_mg_oral_node",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_mg_guile_node": DialogueNode(
            id="vanya_mg_guile_node",
            speaker_name="Sister Vanya",
            text=(
                "Your skilled fingertips tease the soft, damp crease of her inner thighs before sliding upward to caress her glistening bud. "
                "Vanya arches her back with an involuntary, wanton gasp, her fingers clutching your arms. 'Ah... wanderer! It burns... so good...'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_mg_to_climax",
                    text="Drive the ecstasy to its peak: enter her deeply and bring her to overwhelming release!",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "vanya_mg_sinew_node": DialogueNode(
            id="vanya_mg_sinew_node",
            speaker_name="Sister Vanya",
            text=(
                "You grip her slender waist with uncompromising strength, pressing your hardening length between her wet thighs. "
                "Her breath turns into a ragged moan against your neck as you claim her lips in a bruising, heated kiss that leaves her dizzy with desire."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_mg_to_climax2",
                    text="Lift her legs over your shoulders and drive in to claim her climax!",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "vanya_mg_lucidity_node": DialogueNode(
            id="vanya_mg_lucidity_node",
            speaker_name="Sister Vanya",
            text=(
                "'You are not sinning, Vanya,' you murmur into her ear. 'This is the only holy thing left in this dying world.' "
                "Tears of cathartic ecstasy spill from her eyes as your hands rhythmically soothe and stimulate her wet, trembling center, "
                "shattering every lingering vestige of religious guilt."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_mg_to_climax3",
                    text="Slide inside her welcoming warmth for the final, breathless ascension!",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "vanya_mg_oral_node": DialogueNode(
            id="vanya_mg_oral_node",
            speaker_name="Sister Vanya",
            text=(
                "Kneeling between her parted thighs, you part her glistening folds with your fingers and taste her intimate sweetness. "
                "Vanya cries out in sheer disbelief, her fingers tangling frantically in your hair as her hips buck upward against your mouth. "
                "'Merciful martyrs... please! I can't... I'm losing my mind!'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_mg_to_climax4",
                    text="Rise up and sheath yourself inside her drenched core to finish together!",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
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
                "She shivers not from cold, but from sheer sensory overload as your hands cup her waist."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_tender",
                    text="Gently push the chemise off her shoulders and kiss down her throat to her breasts.",
                    next_node="vanya_eroge_foreplay_tender",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_vanya_eroge_dominant",
                    text="Lift her bodily onto the stone altar, parting her bare thighs before you.",
                    next_node="vanya_eroge_foreplay_dominant",
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
                "She whimpers, grinding her hips into your palm with uninhibited hunger."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_enter_tender",
                    text="Align your hips with hers and push smoothly into her velvet warmth.",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_foreplay_dominant": DialogueNode(
            id="vanya_eroge_foreplay_dominant",
            speaker_name="Sister Vanya",
            text=(
                "You lift her onto the altar slab, her smooth bare thighs spreading wide in the candlelight. Stepping between them, you grasp her hips, "
                "your thumbs stroking the damp heat of her inner thighs. Her eyes darken with submission and desire. "
                "'Do with me as you will, wanderer,' she whispers raggedly. 'Cleanse me of this dreadful silence.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_enter_dom",
                    text="Thrust deeply into her tight, glistening depths with fierce, possessive rhythm.",
                    next_node="vanya_eroge_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        "vanya_eroge_climax": DialogueNode(
            id="vanya_eroge_climax",
            speaker_name="Sister Vanya",
            text=(
                "Sheathing yourself completely within her snug, shuddering core, a guttural groan escapes your chest as her tight walls clench around you. "
                "Vanya throws her head back, her ivory throat exposed, gasping in breathless ecstasy as you begin a relentless, driving cadence. "
                "Each deep stroke draws wanton cries from the chirurgeon's lips, echoing softly off the ancient chantry stones. "
                "Her legs wrap tightly around your waist, pulling you deeper, her slick center milking you with urgent spasms. "
                "With a final, desperate cry into your neck, she shatters into a violent, toe-curling climax, her inner muscles clamping fiercely "
                "as you pour your hot release deep inside her, collapsing together into breathless, sweat-slicked communion."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_eroge_afterglow",
                    text="Hold her gently as your breathing slows in the warm candlelight.",
                    next_node="vanya_eroge_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Sister Vanya's Embroidered Rosary"
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
                    id="c_vanya_post_intimacy_recruit",
                    text="'You belong with me now, Vanya. Take up your chirurgeon kit and let us break through the perimeter.'",
                    next_node="vanya_recruited",
                    relationship_change=20
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

        # --- Eroge Spicy Multi-Stage Intimacy Sequence: Madame Silve ---
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
                    id="c_silve_eroge_boudoir",
                    text="Embrace her against the cushions and taste the spiced wine on her lips.",
                    next_node="silve_eroge_boudoir",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_minigame_start",
                    text="Engage in the 'Velvet & Vice' Intimacy Minigame.",
                    next_node="silve_eroge_minigame_start",
                    is_intimacy_action=True,
                    relationship_change=20
                )
            ]
        ),
        "silve_eroge_minigame_start": DialogueNode(
            id="silve_eroge_minigame_start",
            speaker_name="Madame Silve",
            text=(
                "Silve kicks off her satin slippers and pulls you down atop the velvet cushions, her lace chemise riding up her voluptuous, silky hips. "
                "Her dark eyes sparkle with erotic anticipation as her warm thighs cradle your waist. "
                "(The Intimacy Minigame has begun! Build her Arousal to 100% using tactile caresses, commanding rhythm, and decadent kisses)."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_mg_guile",
                    text="[Guile] Erogenous Caress: Tease the silken curve of her hips and stroke her wet core through sheer lace.",
                    next_node="silve_mg_guile_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_mg_sinew",
                    text="[Sinew] Commanding Rhythm: Seize her wrists above her head and press into her with unyielding intensity.",
                    next_node="silve_mg_sinew_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_mg_wine",
                    text="Spiced Wine Kiss: Sip wine from her goblet and pour it down her cleavage, licking every drop.",
                    next_node="silve_mg_wine_node",
                    is_intimacy_action=True
                ),
                DialogueChoice(
                    id="c_silve_mg_oral",
                    text="Devoted Oral Seduction: Kneel amidst the crimson silks and worship her wet, parted lips.",
                    next_node="silve_mg_oral_node",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_mg_guile_node": DialogueNode(
            id="silve_mg_guile_node",
            speaker_name="Madame Silve",
            text=(
                "Your nimble fingers peel aside her gossamer lace underwear. Finding her drenched and burning with desire, you trace her sensitive folds "
                "with exquisite technique. Silve bites her lip, her hips lifting greedily into your hand. 'Mmm... you touch a woman like a master thief, darling...'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_mg_to_climax",
                    text="Take her on the velvet cushions and drive her into ecstasy!",
                    next_node="silve_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "silve_mg_sinew_node": DialogueNode(
            id="silve_mg_sinew_node",
            speaker_name="Madame Silve",
            text=(
                "You pin the proud secret broker to the pillows, your muscular weight pressing against her soft curves. "
                "Her breath catches in her throat; for all her calculating cunning, she melts completely beneath your masculine dominance, "
                "wrapping her silken legs eagerly around your waist."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_mg_to_climax2",
                    text="Thrust deeply into her tight, wet depths and conquer her pleasure!",
                    next_node="silve_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "silve_mg_wine_node": DialogueNode(
            id="silve_mg_wine_node",
            speaker_name="Madame Silve",
            text=(
                "You pour a stream of dark, spiced plum wine across her throat and between her full breasts. Your hot tongue trails down her skin, "
                "drinking the fragrant liquor from her skin. Silve writhes beneath you, moaning your name in sheer sensory delirium."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_mg_to_climax3",
                    text="Push into her drenched center to share the intoxicating finish!",
                    next_node="silve_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "silve_mg_oral_node": DialogueNode(
            id="silve_mg_oral_node",
            speaker_name="Madame Silve",
            text=(
                "Burrowing between her soft, perfumed thighs, your tongue lavishes her swollen clitoris with decadent suction and rhythm. "
                "Silve cries out in wanton abandon, her composure shattering into desperate gasps as she tangles her fingers in your hair, "
                "begging for your steel."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_mg_to_climax4",
                    text="Rise up and bury your length to the hilt within her!",
                    next_node="silve_eroge_climax",
                    is_intimacy_action=True,
                    relationship_change=25
                )
            ]
        ),
        "silve_eroge_boudoir": DialogueNode(
            id="silve_eroge_boudoir",
            speaker_name="Madame Silve",
            text=(
                "She pulls you onto the velvet mattress, straddling your lap with a breathless purr. Her bare breasts, full and warm, "
                "brush against your chest as she unfastens your trousers with hungry, practiced fingers. "
                "'No politics tonight, wanderer,' she whispers against your ear, her teeth gently tugging your earlobe. "
                "'Only skin, sweat, and fire.'"
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_take_control",
                    text="Roll her onto her back, spreading her soft legs and sliding inside her slick depths.",
                    next_node="silve_eroge_climax",
                    is_intimacy_action=True
                )
            ]
        ),
        "silve_eroge_climax": DialogueNode(
            id="silve_eroge_climax",
            speaker_name="Madame Silve",
            text=(
                "Entering her completely, you are enveloped in hot, velvet tightness. Silve lets out a loud, breathless cry that reverberates off the silken walls. "
                "Her hips roll against yours in perfect, decadent harmony, matching each deep, powerful thrust. "
                "The friction between your bodies is intoxicating; sweat slicks your chests as the rhythm turns frantic, urgent, and wild. "
                "Her nails bite into your shoulders, her moans turning into ragged sobs of pleasure as her inner walls convulse in an explosive, shuddering climax. "
                "You drive into her to the hilt, spilling your warmth deep inside her with a guttural roar, collapsing into each other amidst the disheveled crimson silks."
            ),
            choices=[
                DialogueChoice(
                    id="c_silve_eroge_afterglow",
                    text="Recline together on the cushions in decadent afterglow.",
                    next_node="silve_eroge_afterglow",
                    is_intimacy_action=True,
                    relationship_change=25,
                    item_reward="Silve's Scented Silk Favor"
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
                    id="c_silve_afterglow_farewell",
                    text="'I will return, Silve. Now I must reach the gate.'",
                    next_node="silve_farewell"
                )
            ]
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
            is_combatant=False,
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
