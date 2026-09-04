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
                "Her white habit is smeared with charcoal and arterial red. 'Another wanderer,' she whispers, voice husky with exhaustion. "
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
                "into your palm, her fingers lingering against your skin, warm and trembling."
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
                "Vanya shivers at your touch. Her skin is feverishly warm. For a moment, her religious composure fractures completely, "
                "revealing a lonely, terrified woman starved of tenderness. 'You are reckless to speak like that in a city awaiting the torch,' "
                "she whispers, though she leans into your hand for a lingering second before looking away."
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
        "vanya_intimacy_scene": DialogueNode(
            id="vanya_intimacy_scene",
            speaker_name="Sister Vanya",
            text=(
                "Behind the tattered altar curtain, cloaked in incense and twilight, Vanya unfastens the high collar of her habit with trembling urgency. "
                "Her breath comes quick and ragged against your throat. In the shadow of inevitable slaughter, all piety and restraint dissolve into raw, "
                "feverish hunger. Her hands grasp your shoulders as your bodies collide, seeking fierce, desperate validation of life in a world "
                "drowning in ash. The encounter leaves you both breathless, skin slick with perspiration, your mind cleared of dread and anchored by profound intimacy."
            ),
            choices=[
                DialogueChoice(
                    id="c_vanya_post_intimacy_recruit",
                    text="'You belong with me now, Vanya. Take up your chirurgeon kit and let us fight our way out.'",
                    next_node="vanya_recruited",
                    relationship_change=20
                )
            ]
        ),
        "vanya_recruited": DialogueNode(
            id="vanya_recruited",
            speaker_name="Sister Vanya",
            text=(
                "Vanya straps an apothecary satchel across her chest and conceals a surgical scalpel in her sleeve. "
                "'My place is at your side, wanderer. I will mend your flesh when you bleed, and I will strike when darkness closes in.'"
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
                    id="c_malakor_vanya_quest",
                    text="'Sister Vanya needs the Wolfsbane Nectar you looted from the chantry. Name your price.'",
                    next_node="malakor_quest_trade",
                    relationship_change=5
                ),
                DialogueChoice(
                    id="c_malakor_court",
                    text="Meet his gaze directly, a slow smirk touching your lips. 'A warrior of your caliber shouldn't waste his final hours drinking alone.'",
                    next_node="malakor_romance_start",
                    is_romance_action=True,
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
                    text="Step into his space, placing a firm hand on his armored chest. 'You don't have to carry this grief alone, Malakor.'",
                    next_node="malakor_intimacy_scene",
                    is_intimacy_action=True,
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
                "He leans forward, close enough that you can smell the sharp tang of rye gin and leather on him. "
                "'Bold words for a wanderer. Most men fear what my hands can do. But you... you're sizing me up like a prize. "
                "Prove you have the stomach to ride the storm with me, and maybe I'll show you what this blade can do in private.'"
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
                "Inside his private armory quarters, away from the roaring fires and drunk mercenaries, Malakor pulls you in with crushing, "
                "ferocious strength. The discarded armor clatters to the flagstones. His muscular, heavily scarred body is burning with heat, "
                "demanding an unfiltered, primal release after months of bloodshed. Your mouths lock in a bruised, heated clash of teeth and tongue. "
                "Every touch is intense, possessive, and raw—two condemned men defying the cold shadow of the executioner's pyre with unbridled passion. "
                "When the frenzy subsides in the dim lantern light, his arm remains wrapped securely around your chest, breathing in sync with yours."
            ),
            choices=[
                DialogueChoice(
                    id="c_malakor_post_intimacy_recruit",
                    text="'Get your greatsword, Malakor. Tonight, we fight as one.'",
                    next_node="malakor_recruited",
                    relationship_change=20
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
                "Her cleavage is accentuated by a corset of black lace and velvet; dark kohl lines her predatory, intelligent eyes. "
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
                "her hand lingering against your thigh."
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
        "silve_intimacy_scene": DialogueNode(
            id="silve_intimacy_scene",
            speaker_name="Madame Silve",
            text=(
                "Behind heavy drawn curtains of midnight velvet, Silve sheds her silks with practiced, intoxicating grace. "
                "The air is thick with sweet opium and musk. She pushes you onto the feather cushions, straddling you with a breathless gasp. "
                "Her touch is exquisite, decadent, and relentless, guiding you into a sensory trance where the doomed world outside ceases to exist. "
                "As the midnight bells reverberate through the floorboards, you lose yourself completely in her intoxicating warmth, "
                "sealing an alliance born of dark pleasure and mutual survival."
            ),
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
                )
            ]
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
            can_romance=True,
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
