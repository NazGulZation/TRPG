"""Game Engine managing state, dialogues, eroge romance, attack-on-sight, party mechanics, and quests."""

import random
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from game.models import Player, NPC, Location, Quest, Stats, Item
from game.data.prologue import (
    get_prologue_locations,
    get_prologue_npcs,
    get_prologue_quests,
    get_prologue_factions,
    get_prologue_metadata,
    get_prologue_items,
    SUITABLE_INTIMACY_LOCATIONS,
)


class GameEngine:
    def __init__(self):
        self.player = Player()
        self.locations: Dict[str, Location] = get_prologue_locations()
        self.npcs: Dict[str, NPC] = get_prologue_npcs()
        self.quests: Dict[str, Quest] = get_prologue_quests()
        self.factions = get_prologue_factions()
        self.items: Dict[str, Item] = get_prologue_items()
        self.logs: List[Dict[str, Any]] = []
        self.current_dialogue: Optional[Dict[str, Any]] = None
        self.combat_state: Optional[Dict[str, Any]] = None
        self.intimacy_state: Optional[Dict[str, Any]] = None
        self.bell_toll: int = 9  # Starts at 9:00 PM, purges at 12:00 Midnight
        self.action_count: int = 0
        self.game_over: bool = False
        self.victory: bool = False
        self.max_party_size: int = 4

        # Initialize prologue opening narrative from configuration
        metadata = get_prologue_metadata()
        opening = metadata.get("opening_log", {
            "category": "prologue",
            "title": "PROLOGUE: ASHEN SOLSTICE - THE SINKING OF OAKHAVEN",
            "text": (
                "You awaken with your face pressed into damp cobbles covered in greasy ash. "
                "The iron brand of the condemned throbs raw and blistering against your neck. "
                "Around you, the quarantine walls of Oakhaven loom like teeth of a blackened maw. "
                "At midnight, the Grand Inquisitor will drop the portcullis and purge the district with white phosphorus. "
                "You have only hours to navigate the squabbling factions, forge desperate alliances, seek solace in the dark, "
                "and find a way beyond the walls before the sky catches fire."
            )
        })
        self.add_log(
            opening.get("category", "prologue"),
            opening.get("title", "PROLOGUE: ASHEN SOLSTICE - THE SINKING OF OAKHAVEN"),
            opening.get("text", "")
        )

    def add_log(self, category: str, title: str, text: str, meta: Optional[Dict[str, Any]] = None):
        self.logs.append({
            "category": category,
            "title": title,
            "text": text,
            "meta": meta or {}
        })

    def advance_clock(self):
        self.action_count += 1
        if self.action_count % 3 == 0 and self.bell_toll < 12:
            self.bell_toll += 1
            hours_left = 12 - self.bell_toll
            if self.bell_toll == 12:
                self.add_log(
                    "bell",
                    "MIDNIGHT BELL TOLLS: THE PURGE COMMENCES",
                    "The watchtower bell tolls twelve deafening strokes! Across the ramparts, Dawnbound catapults launch incandescent phosphorus canisters. You must escape immediately!"
                )
            else:
                self.add_log(
                    "bell",
                    f"Watchtower Bell: {self.bell_toll}:00 PM",
                    f"Distant iron bells reverberate through the toxic fog. Only {hours_left} hour{'s' if hours_left > 1 else ''} remain until midnight!"
                )

    def get_effective_stat(self, stat_name: str) -> int:
        val = getattr(self.player.stats, stat_name, 0)
        # Item passives
        if stat_name == "lucidity" and "Sister Vanya's Embroidered Rosary" in self.player.inventory:
            val += 2
        elif stat_name == "guile" and "Silve's Scented Silk Favor" in self.player.inventory:
            val += 2
        elif stat_name == "sinew" and "Malakor's Drake Whetstone" in self.player.inventory:
            val += 2

        # Party member bonus (1/4 of companion stat added)
        for party_id in self.player.party:
            if party_id in self.npcs:
                val += getattr(self.npcs[party_id].stats, stat_name, 0) // 4
        return val

    def apply_sovereign_discount(self, cost: int) -> int:
        if "Silve's Scented Silk Favor" in self.player.inventory and cost > 0:
            return max(1, int(cost * 0.75))
        return cost

    def adjust_dread(self, amount: int):
        if amount > 0 and "Sister Vanya's Embroidered Rosary" in self.player.inventory:
            amount = max(1, amount // 2)
        self.player.dread = max(0, min(100, self.player.dread + amount))

    def add_inventory_item(self, item_name: str):
        self.player.inventory.append(item_name)
        if item_name == "Wolfsbane Nectar":
            q = self.quests.get("q_mercy_hemlock")
            if q and q.current_stage in (0, 1):
                q.current_stage = 2
                self.add_log(
                    "quest",
                    f"Quest Updated: {q.title}",
                    "You have acquired the Wolfsbane Nectar. Deliver it to Sister Vanya in the Ruined Chantry."
                )
        elif item_name == "Loras's Iron Signet":
            q = self.quests.get("q_blood_brass")
            if q and q.current_stage in (0, 1):
                q.current_stage = 2
                self.add_log(
                    "quest",
                    f"Quest Updated: {q.title}",
                    "You recovered Loras's Iron Signet. Return it to Commander Malakor at the Iron Drake Bastion."
                )
        elif item_name == "Turnkey's Stolen Ledger":
            q = self.quests.get("q_silk_cyanide")
            if q and q.current_stage in (0, 1):
                q.current_stage = 2
                self.add_log(
                    "quest",
                    f"Quest Updated: {q.title}",
                    "You secured the Turnkey's Stolen Ledger. Deliver it to Madame Silve at the Gilded Rat Parlour."
                )

    def get_item(self, key: str) -> Optional[Item]:
        """Look up item definition by ID or display name."""
        return self.items.get(key)

    def use_item(self, item_name: str) -> Dict[str, Any]:
        """Activate usable items directly from player inventory."""
        if item_name not in self.player.inventory:
            return {"error": f"You do not possess {item_name}."}

        item = self.get_item(item_name)
        if not item or not item.is_usable:
            return {"error": f"{item_name} has no immediate active use here."}

        if item.effect_type == "dread_relief":
            relief = item.effect_value if item.effect_value else 10
            self.adjust_dread(-relief)
            log_title = f"Used {item.name}"
            log_text = item.effect_description or f"Using {item.name} drives back the dread (-{relief} Dread)."
            self.add_log("item", log_title, log_text)
            return self.get_state()

        elif item.effect_type == "combat_buff":
            log_title = f"Prepared {item.name}"
            log_text = item.effect_description or f"You hone your weapon with {item.name} for combat."
            self.add_log("item", log_title, log_text)
            return self.get_state()

        elif item.effect_type == "heal":
            heal = item.effect_value if item.effect_value else 15
            self.player.current_hp = min(self.player.max_hp, self.player.current_hp + heal)
            log_title = f"Used {item.name}"
            log_text = item.effect_description or f"You restore {heal} HP."
            self.add_log("item", log_title, log_text)
            return self.get_state()

        return {"error": f"{item_name} has no immediate active use here."}

    def can_initiate_companion_erotic(self, npc_id: str) -> bool:
        """Check if companion is eligible for initiating an erotic scene in the current location."""
        if npc_id not in self.player.party or self.combat_state:
            return False
        npc = self.npcs.get(npc_id)
        if not npc or npc.gender != "female" or not npc.can_romance:
            return False
        allowed = SUITABLE_INTIMACY_LOCATIONS.get(npc_id, [])
        return self.player.current_location_id in allowed

    def get_state(self) -> Dict[str, Any]:
        curr_loc = self.locations.get(self.player.current_location_id)
        loc_npcs = []
        if curr_loc:
            for npc_id in curr_loc.npc_ids:
                if npc_id in self.npcs and not self.npcs[npc_id].is_dead and not self.npcs[npc_id].is_in_party:
                    npc = self.npcs[npc_id]
                    loc_npcs.append({
                        "id": npc.id,
                        "name": npc.name,
                        "title": npc.title,
                        "gender": npc.gender,
                        "relationship": npc.relationship,
                        "is_combatant": npc.is_combatant,
                        "can_romance": npc.can_romance,
                        "can_recruit": getattr(npc, "can_recruit", True),
                        "is_romanced": npc.is_romanced,
                        "stats": npc.stats.to_dict(),
                        "description": npc.description
                    })

        party_members = []
        for p_id in self.player.party:
            if p_id in self.npcs:
                npc = self.npcs[p_id]
                party_members.append({
                    "id": npc.id,
                    "name": npc.name,
                    "title": npc.title,
                    "stats": npc.stats.to_dict(),
                    "hp": npc.current_hp,
                    "max_hp": npc.max_hp,
                    "is_romanced": npc.is_romanced,
                    "gender": npc.gender,
                    "can_romance": npc.can_romance,
                    "relationship": npc.relationship,
                    "can_initiate_erotic": self.can_initiate_companion_erotic(npc.id)
                })

        active_quests = []
        for q_id, q in self.quests.items():
            if q.current_stage > 0 and q.current_stage != 99:
                stage_info = q.stages.get(q.current_stage)
                active_quests.append({
                    "id": q.id,
                    "title": q.title,
                    "description": q.description,
                    "current_stage": q.current_stage,
                    "stage_description": stage_info.description if stage_info else ""
                })

        effective_stats = {
            "sinew": self.get_effective_stat("sinew"),
            "guile": self.get_effective_stat("guile"),
            "lucidity": self.get_effective_stat("lucidity")
        }

        inventory_items = []
        for itm_name in self.player.inventory:
            itm_obj = self.get_item(itm_name)
            inventory_items.append({
                "name": itm_name,
                "is_usable": itm_obj.is_usable if itm_obj else False,
                "description": itm_obj.description if itm_obj else "",
                "item_type": itm_obj.item_type if itm_obj else "quest"
            })

        return {
            "player": {
                "name": self.player.name,
                "gender": self.player.gender,
                "title": self.player.title,
                "stats": effective_stats,
                "base_stats": self.player.stats.to_dict(),
                "hp": self.player.current_hp,
                "max_hp": self.player.max_hp,
                "dread": self.player.dread,
                "sovereigns": self.player.sovereigns,
                "inventory": self.player.inventory,
                "inventory_details": inventory_items,
                "party": party_members,
                "romanced": self.player.romanced_npcs,
                "factions": self.player.faction_reputation
            },
            "usable_items": list({itm.name for itm in self.items.values() if itm.is_usable}),
            "location": {
                "id": curr_loc.id if curr_loc else "",
                "name": curr_loc.name if curr_loc else "",
                "subtitle": curr_loc.subtitle if curr_loc else "",
                "description": curr_loc.description if curr_loc else "",
                "faction_id": curr_loc.faction_id if curr_loc else "",
                "connected": [
                    {"id": loc_id, "name": self.locations[loc_id].name}
                    for loc_id in curr_loc.connected_locations if loc_id in self.locations
                ] if curr_loc else [],
                "npcs": loc_npcs,
                "ground_items": curr_loc.items_on_ground if curr_loc else []
            },
            "factions": self.factions,
            "active_quests": active_quests,
            "dialogue": self.current_dialogue,
            "combat": self.combat_state,
            "intimacy": self.intimacy_state,
            "bell_toll": self.bell_toll,
            "logs": self.logs[-25:],
            "game_over": self.game_over,
            "victory": self.victory,
            "max_party_size": self.max_party_size
        }

    def travel(self, destination_id: str) -> Dict[str, Any]:
        if self.combat_state:
            return {"error": "You cannot flee while engaged in life-or-death combat!"}

        curr_loc = self.locations.get(self.player.current_location_id)
        if not curr_loc or destination_id not in curr_loc.connected_locations:
            return {"error": "Path is obstructed or unreachable."}

        self.player.current_location_id = destination_id
        dest = self.locations[destination_id]
        self.current_dialogue = None
        self.intimacy_state = None
        self.advance_clock()

        self.add_log(
            "travel",
            f"Arrived at {dest.name}",
            dest.description
        )

        # Check Attack-on-Sight for any NPC present with relationship <= -50
        for npc_id in dest.npc_ids:
            if npc_id in self.npcs:
                npc = self.npcs[npc_id]
                if not npc.is_dead and not npc.is_in_party and npc.relationship <= -50:
                    self.start_combat(npc_id, ambush=True)
                    break

        return self.get_state()

    def inspect_ground(self) -> Dict[str, Any]:
        curr_loc = self.locations.get(self.player.current_location_id)
        if not curr_loc:
            return {"error": "Unknown location."}

        self.advance_clock()
        found = []
        if curr_loc.items_on_ground:
            for itm in list(curr_loc.items_on_ground):
                self.add_inventory_item(itm)
                curr_loc.items_on_ground.remove(itm)
                found.append(itm)

        # Quest specific find
        if curr_loc.id == "gallow_square":
            q = self.quests.get("q_blood_brass")
            if q and q.current_stage == 1 and "Loras's Iron Signet" not in self.player.inventory:
                self.add_inventory_item("Loras's Iron Signet")
                self.add_log(
                    "item",
                    "Discovered Loras's Iron Signet",
                    "Sifting through the charred bones of the ash urns, your fingers clasp a heavy blackened signet ring bearing the Drake crest."
                )
                return self.get_state()

        if found:
            self.add_log(
                "item",
                "Items Scavenged",
                f"You scavenged: {', '.join(found)}."
            )
        else:
            self.add_log(
                "narrative",
                "Scouring the Shadowed Rubble",
                "You search the grime, broken timbers, and pooled filth, but find nothing of value left."
            )

        return self.get_state()

    def talk_npc(self, npc_id: str) -> Dict[str, Any]:
        if self.combat_state:
            return {"error": "You cannot converse in the heat of combat!"}

        if npc_id not in self.npcs:
            return {"error": "NPC does not exist."}

        npc = self.npcs[npc_id]
        if npc.is_dead:
            return {"error": "They lie dead before you."}

        # If extremely hostile, attack on sight instead!
        if npc.relationship <= -50:
            self.start_combat(npc_id, ambush=True)
            return self.get_state()

        # If in party, route directly to their companion dialogue hub
        if npc.is_in_party:
            node_id = self.get_companion_hub_id(npc)
            if node_id in npc.dialogue_nodes:
                self.load_dialogue_node(npc, node_id)
                return self.get_state()

        # Build dynamic dialogue
        node_id = npc.dialogue_root
        if npc.id == "sister_vanya":
            q = self.quests.get("q_mercy_hemlock")
            if q:
                if "Wolfsbane Nectar" in self.player.inventory:
                    q.current_stage = 2
                    node_id = "vanya_quest_complete"
                elif q.current_stage == 99:
                    node_id = "vanya_quest_complete"
                elif q.current_stage == 1:
                    node_id = "vanya_quest_accepted"
        elif npc.id == "commander_malakor":
            q = self.quests.get("q_blood_brass")
            if q:
                if "Loras's Iron Signet" in self.player.inventory:
                    q.current_stage = 2
                    node_id = "malakor_quest_complete"
                elif q.current_stage == 99:
                    node_id = "malakor_quest_complete"
                elif q.current_stage == 1:
                    node_id = "malakor_quest_accepted"
        elif npc.id == "madame_silve":
            q = self.quests.get("q_silk_cyanide")
            if q:
                if "Turnkey's Stolen Ledger" in self.player.inventory:
                    q.current_stage = 2
                    node_id = "silve_quest_complete"
                elif q.current_stage == 99:
                    node_id = "silve_quest_complete"
                elif q.current_stage == 1:
                    node_id = "silve_quest_accepted"
        elif npc.id == "little_toby":
            if npc.relationship <= -20:
                node_id = "toby_robbed"
            elif npc.relationship >= 20 or "Master Sluice Key" in self.player.inventory or "Turnkey's Stolen Ledger" in self.player.inventory:
                node_id = "toby_saved"

        self.load_dialogue_node(npc, node_id)
        return self.get_state()

    def load_dialogue_node(self, npc: NPC, node_id: str):
        node = npc.dialogue_nodes.get(node_id)
        if not node:
            self.current_dialogue = None
            return

        formatted_choices = []
        for ch in node.choices:
            # If in party and this choice initiates an intimate scene, only display if in a suitable location
            if npc.is_in_party and ch.is_intimacy_action and not self.can_initiate_companion_erotic(npc.id):
                continue

            stat_met = True
            if ch.required_stat:
                p_stat = self.get_effective_stat(ch.required_stat)
                stat_met = p_stat >= ch.required_value

            item_met = True
            if ch.item_required and ch.item_required not in self.player.inventory:
                item_met = False

            sovereigns_met = True
            effective_cost = self.apply_sovereign_discount(ch.sovereign_cost)
            if effective_cost > 0 and self.player.sovereigns < effective_cost:
                sovereigns_met = False

            display_text = ch.text
            if ch.sovereign_cost > 0 and effective_cost < ch.sovereign_cost:
                display_text += f" [Discounted: {effective_cost} Sov]"

            formatted_choices.append({
                "id": ch.id,
                "text": display_text,
                "stat_met": stat_met,
                "item_met": item_met,
                "sovereigns_met": sovereigns_met,
                "is_romance": ch.is_romance_action,
                "is_intimacy": ch.is_intimacy_action,
                "is_hostile": ch.is_hostile_action,
            })

        self.current_dialogue = {
            "npc_id": npc.id,
            "npc_name": npc.name,
            "npc_title": npc.title,
            "speaker": node.speaker_name,
            "text": node.text,
            "current_node": node.id,
            "choices": formatted_choices
        }

    def choose_dialogue(self, choice_id: str) -> Dict[str, Any]:
        if not self.current_dialogue:
            return {"error": "No active conversation."}

        npc_id = self.current_dialogue["npc_id"]
        npc = self.npcs.get(npc_id)
        if not npc:
            return {"error": "NPC not found."}

        curr_node_id = self.current_dialogue["current_node"]
        curr_node = npc.dialogue_nodes.get(curr_node_id)
        if not curr_node:
            return {"error": "Dialogue node lost."}

        chosen_choice: Optional[DialogueChoice] = None
        for ch in curr_node.choices:
            if ch.id == choice_id:
                chosen_choice = ch
                break

        if not chosen_choice:
            return {"error": "Invalid choice."}

        # Check stat requirements using effective stats
        if chosen_choice.required_stat:
            p_stat_val = self.get_effective_stat(chosen_choice.required_stat)
            if p_stat_val < chosen_choice.required_value:
                if chosen_choice.failure_node:
                    self.load_dialogue_node(npc, chosen_choice.failure_node)
                    return self.get_state()
                else:
                    return {"error": f"Requires {chosen_choice.required_stat.capitalize()} {chosen_choice.required_value}."}

        # Check sovereign cost with silk discount
        effective_cost = self.apply_sovereign_discount(chosen_choice.sovereign_cost)
        if effective_cost > 0:
            if self.player.sovereigns < effective_cost:
                return {"error": f"Requires {effective_cost} Sovereigns (You have {self.player.sovereigns})."}
            self.player.sovereigns -= effective_cost
            self.add_log("item", "Sovereigns Paid", f"You paid {effective_cost} Sovereigns.")

        # Check required item
        if chosen_choice.item_required:
            if chosen_choice.item_required not in self.player.inventory:
                return {"error": f"Requires item: {chosen_choice.item_required}"}
            self.player.inventory.remove(chosen_choice.item_required)

        # Apply rewards
        rewards = []
        if chosen_choice.item_reward:
            rewards.append(chosen_choice.item_reward)
        if chosen_choice.item_rewards:
            rewards.extend(chosen_choice.item_rewards)

        for rew in rewards:
            if rew not in self.player.inventory:
                self.add_inventory_item(rew)
                self.add_log("item", f"Received {rew}", f"You acquired: {rew}.")

        # Adjust relationship
        if chosen_choice.relationship_change != 0:
            npc.relationship = max(-100, min(100, npc.relationship + chosen_choice.relationship_change))
            sign = "+" if chosen_choice.relationship_change > 0 else ""
            self.add_log(
                "relationship",
                f"{npc.name} Disposition ({sign}{chosen_choice.relationship_change})",
                f"Your standing with {npc.name} is now {npc.relationship}/100."
            )

        # Adjust faction
        for f_id, f_val in chosen_choice.faction_changes.items():
            if f_id in self.player.faction_reputation:
                self.player.faction_reputation[f_id] += f_val
                sign = "+" if f_val > 0 else ""
                self.add_log(
                    "faction",
                    f"Faction Standing ({sign}{f_val})",
                    f"Standing with {self.factions.get(f_id, {}).get('name', f_id)} changed."
                )

        # Handle quests
        if chosen_choice.quest_trigger:
            q = self.quests.get(chosen_choice.quest_trigger)
            if q:
                q.current_stage = chosen_choice.quest_stage_set or 1
                self.add_log(
                    "quest",
                    f"Quest Active: {q.title}",
                    q.description
                )

        # Complete Quest Turn-in check
        if curr_node_id in ("vanya_quest_complete", "malakor_quest_complete", "silve_quest_complete"):
            q_map = {
                "vanya_quest_complete": "q_mercy_hemlock",
                "malakor_quest_complete": "q_blood_brass",
                "silve_quest_complete": "q_silk_cyanide"
            }
            q_id = q_map.get(curr_node_id)
            if q_id and q_id in self.quests:
                quest = self.quests[q_id]
                if quest.current_stage != 99:
                    quest.current_stage = 99
                    for st_id, st_obj in quest.stages.items():
                        if st_obj.required_item and st_obj.required_item in self.player.inventory:
                            self.player.inventory.remove(st_obj.required_item)
                    self.player.sovereigns += quest.reward_sovereigns
                    for rew_item in quest.reward_items:
                        if rew_item not in self.player.inventory:
                            self.add_inventory_item(rew_item)
                    if quest.faction_id in self.player.faction_reputation:
                        self.player.faction_reputation[quest.faction_id] += quest.reward_faction_points
                    npc.relationship = min(100, npc.relationship + quest.reward_relation)
                    self.add_log(
                        "quest_complete",
                        f"Quest Completed: {quest.title}",
                        f"{quest.completion_text} (Earned {quest.reward_sovereigns} sovereigns, items: {', '.join(quest.reward_items)})."
                    )

        # Handle Heterosexual Romance Intimacy Encounter (Female NPCs only)
        if chosen_choice.is_intimacy_action and npc.gender == "female" and npc.can_romance:
            npc.is_romanced = True
            if npc.id not in self.player.romanced_npcs:
                self.player.romanced_npcs.append(npc.id)
            # Intimacy eradicates dread completely
            self.player.dread = 0
            self.add_log(
                "romance",
                f"Solace of the Flesh: {npc.name}",
                f"You shared an ecstatic, passionate encounter with {npc.name}. All creeping terror of the purge is banished into calm (Dread reduced to 0)."
            )

            # Award unique keepsakes
            if npc.id == "sister_vanya" and "Sister Vanya's Embroidered Rosary" not in self.player.inventory:
                self.add_inventory_item("Sister Vanya's Embroidered Rosary")
            elif npc.id == "madame_silve" and "Silve's Scented Silk Favor" not in self.player.inventory:
                self.add_inventory_item("Silve's Scented Silk Favor")
                self.player.sovereigns += 35

        # Handle Companion Special Interactions
        if chosen_choice.id == "c_vanya_companion_tend":
            heal = 15
            self.player.current_hp = min(self.player.max_hp, self.player.current_hp + heal)
            self.adjust_dread(-10)
            self.add_log("party", "Sister Vanya Tended Wounds", f"Vanya cleans and binds your wounds (+{heal} HP, -10 Dread).")

        elif chosen_choice.id == "c_silve_companion_contraband":
            self.player.sovereigns += 20
            self.add_log("item", "Received Contraband Sovereigns", "Silve slips a purse of 20 Sovereigns into your hand with a sly wink.")

        elif chosen_choice.id == "c_malakor_companion_drink":
            self.adjust_dread(-5)
            self.add_log("party", "Shared Drake Rye", "You and Malakor share a burning swig of rye gin (-5 Dread).")

        elif chosen_choice.id in ("c_vanya_confirm_dismiss", "c_malakor_confirm_dismiss", "c_silve_confirm_dismiss"):
            self.dismiss_party(npc.id)

        # Handle Male Commander Malakor Blood-Brotherhood (Non-romance)
        if npc.id == "commander_malakor" and chosen_choice.id == "c_malakor_embrace":
            if "Malakor's Drake Whetstone" not in self.player.inventory:
                self.add_inventory_item("Malakor's Drake Whetstone")
            self.add_log(
                "party",
                "Blood-Brothers of the Iron Drake",
                "You swore an unyielding blood-oath with Commander Malakor. He presented you with his Drake Whetstone (+2 Sinew, +4 combat damage)."
            )

        # Handle Hostility trigger
        if chosen_choice.is_hostile_action or npc.relationship <= -50:
            self.current_dialogue = None
            self.start_combat(npc.id, ambush=False)
            return self.get_state()

        self.advance_clock()
        next_node_id = chosen_choice.next_node
        if next_node_id in ("vanya_recruited", "malakor_recruited", "silve_recruited"):
            self.recruit_party(npc.id)

        # Dynamic location-unique routing when initiating companion intimacy
        if npc.is_in_party and next_node_id in ("vanya_companion_intimacy_start", "silve_companion_intimacy_start"):
            loc_scene = self.get_companion_erotic_node_id(npc)
            if loc_scene and loc_scene in npc.dialogue_nodes:
                next_node_id = loc_scene

        self.load_dialogue_node(npc, next_node_id)
        return self.get_state()

    def get_companion_hub_id(self, npc: NPC) -> str:
        short_id = npc.id.replace("sister_", "").replace("commander_", "").replace("madame_", "")
        candidates = [
            f"{short_id}_companion_hub",
            f"{npc.id}_companion_hub"
        ]
        for c in candidates:
            if c in npc.dialogue_nodes:
                return c
        return npc.dialogue_root

    def get_companion_erotic_node_id(self, npc: NPC, location_id: Optional[str] = None) -> Optional[str]:
        curr_loc = location_id or self.player.current_location_id

        # Location-unique scene mappings
        location_scenes = {
            "sister_vanya": {
                "ruined_chantry": "vanya_chantry_step1_initiate",
                "gilded_rat": "vanya_gilded_step1_initiate"
            },
            "madame_silve": {
                "gilded_rat": "silve_gilded_step1_initiate"
            }
        }
        if npc.id in location_scenes and curr_loc in location_scenes[npc.id]:
            target_node = location_scenes[npc.id][curr_loc]
            if target_node in npc.dialogue_nodes:
                return target_node

        short_id = npc.id.replace("sister_", "").replace("commander_", "").replace("madame_", "")
        candidates = [
            f"{short_id}_companion_intimacy_start",
            f"{npc.id}_companion_intimacy_start",
            f"{short_id}_intimacy_scene",
            f"{npc.id}_intimacy_scene"
        ]
        for c in candidates:
            if c in npc.dialogue_nodes:
                return c
        return None

    # --- Party Companion Intimacy & Erotic Scenes ---
    def start_party_erotic_scene(self, npc_id: str) -> Dict[str, Any]:
        """Initiate a lengthy, explicit narrative erotic scene with an adult female companion in a suitable location."""
        if self.combat_state:
            return {"error": "You cannot seek carnal solace during life-or-death battle!"}

        if npc_id not in self.npcs:
            return {"error": "Character not found."}

        npc = self.npcs[npc_id]
        if npc_id not in self.player.party:
            return {"error": f"{npc.name} is not in your party."}

        if npc.gender != "female" or not npc.can_romance:
            return {"error": f"{npc.name} cannot be courted intimately."}

        if not self.can_initiate_companion_erotic(npc_id):
            curr_loc = self.locations.get(self.player.current_location_id)
            loc_name = curr_loc.name if curr_loc else "This area"
            return {"error": f"{loc_name} is not suitable for an intimate encounter with {npc.name}. Seek a secluded haven such as the Chantry or the Gilded Rat."}

        scene_node = self.get_companion_erotic_node_id(npc)
        if scene_node and scene_node in npc.dialogue_nodes:
            self.load_dialogue_node(npc, scene_node)
            return self.get_state()

        return {"error": "Intimate scene not found."}

    def start_intimacy(self, npc_id: str) -> Dict[str, Any]:
        """Alias for starting party companion erotic scene."""
        return self.start_party_erotic_scene(npc_id)

    def start_intimacy_minigame(self, npc_id: str) -> Dict[str, Any]:
        """Compatibility method routing directly into the narrative erotic scene."""
        return self.start_party_erotic_scene(npc_id)

    def intimacy_action(self, technique: str) -> Dict[str, Any]:
        return self.get_state()

    def close_intimacy(self) -> Dict[str, Any]:
        self.intimacy_state = None
        return self.get_state()

    def close_dialogue(self) -> Dict[str, Any]:
        self.current_dialogue = None
        return self.get_state()

    def recruit_party(self, npc_id: str) -> Dict[str, Any]:
        if npc_id not in self.npcs:
            return {"error": "Character not found."}
        npc = self.npcs[npc_id]

        if not getattr(npc, "can_recruit", True):
            return {"error": f"{npc.name} cannot be recruited into your traveling party."}

        if not npc.is_combatant:
            return {"error": f"{npc.name} is too frail or unfit for battle and cannot join the frontlines."}

        if npc.relationship < 50:
            return {"error": f"{npc.name} does not trust you enough to fight at your side (Requires 50+ Relationship, current: {npc.relationship})."}

        if npc.is_in_party:
            return {"error": f"{npc.name} is already in your party."}

        if len(self.player.party) >= self.max_party_size:
            return {"error": f"Party is full (maximum {self.max_party_size} companions)."}

        npc.is_in_party = True
        self.player.party.append(npc.id)
        self.add_log(
            "party",
            f"{npc.name} Joined the Party!",
            f"{npc.name} ({npc.title}) now travels at your side, lending their stats and steel."
        )
        return self.get_state()

    def dismiss_party(self, npc_id: str) -> Dict[str, Any]:
        if npc_id in self.player.party:
            self.player.party.remove(npc_id)
            if npc_id in self.npcs:
                self.npcs[npc_id].is_in_party = False
            self.add_log(
                "party",
                "Companion Dismissed",
                f"{self.npcs[npc_id].name if npc_id in self.npcs else 'Companion'} has returned to waiting in the district."
            )
        return self.get_state()

    # --- Combat Engine ---
    def start_combat(self, npc_id: str, ambush: bool = False):
        npc = self.npcs.get(npc_id)
        if not npc or npc.is_dead:
            return

        self.current_dialogue = None
        self.intimacy_state = None
        self.combat_state = {
            "npc_id": npc.id,
            "npc_name": npc.name,
            "npc_hp": npc.current_hp,
            "npc_max_hp": npc.max_hp,
            "npc_stats": npc.stats.to_dict(),
            "turn": 1,
            "combat_log": []
        }

        if ambush:
            self.combat_state["combat_log"].append(
                f"ATTACK ON SIGHT! Blinding hatred burns in {npc.name}'s eyes! They brandish their steel and lunge at you without warning!"
            )
            dmg = max(4, npc.stats.sinew // 2 + random.randint(1, 4))
            self.player.current_hp = max(0, self.player.current_hp - dmg)
            self.combat_state["combat_log"].append(
                f"{npc.name} lands an ambush strike for {dmg} physical damage!"
            )
            if self.player.current_hp <= 0:
                self.game_over = True
                self.add_log("death", "Slain in an Ambush", f"You fell beneath the wrath of {npc.name}.")

        self.add_log(
            "combat",
            f"BATTLE ENGAGED: {npc.name}",
            f"You are locked in lethal combat against {npc.name} ({npc.title})."
        )

    def combat_action(self, action_type: str) -> Dict[str, Any]:
        """Action types: 'sinew_strike', 'guile_skirmish', 'lucidity_feint', 'use_bandage'"""
        if not self.combat_state:
            return {"error": "Not currently in combat."}

        npc_id = self.combat_state["npc_id"]
        npc = self.npcs.get(npc_id)
        if not npc:
            self.combat_state = None
            return self.get_state()

        log_lines = []

        # Companion bonus
        companion_bonus_dmg = 0
        for p_id in self.player.party:
            if p_id in self.npcs:
                c = self.npcs[p_id]
                c_dmg = max(2, c.stats.sinew // 3)
                companion_bonus_dmg += c_dmg
                log_lines.append(f"{c.name} strikes with their weapon, inflicting {c_dmg} damage!")

        # Equipment Buffs
        total_gear_dmg = 4 if "Malakor's Drake Whetstone" in self.player.inventory else 0

        # Player Action Resolution
        p_sinew = self.get_effective_stat("sinew")
        p_guile = self.get_effective_stat("guile")
        p_luc = self.get_effective_stat("lucidity")

        if action_type == "sinew_strike":
            diff = p_sinew - npc.stats.sinew + random.randint(-2, 4)
            if diff >= 0:
                dmg = max(6, p_sinew // 2 + random.randint(2, 6)) + companion_bonus_dmg + total_gear_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Sinew] You overpower {npc.name}'s guard, driving iron deep into flesh for {dmg} damage!")
            else:
                dmg = max(2, random.randint(1, 3)) + companion_bonus_dmg + total_gear_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Sinew] {npc.name} braces against your assault. You inflict {dmg} glancing damage.")

        elif action_type == "guile_skirmish":
            diff = p_guile - npc.stats.guile + random.randint(-2, 4)
            if diff >= 0:
                dmg = max(8, int(p_guile * 0.7) + random.randint(3, 7)) + companion_bonus_dmg + total_gear_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Guile] Slipping through the shadows, your blade pierces an unarmored seam for {dmg} critical damage!")
            else:
                dmg = 3 + companion_bonus_dmg + total_gear_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Guile] {npc.name} tracks your feint. You land only {dmg} scratch damage.")

        elif action_type == "lucidity_feint":
            diff = p_luc - npc.stats.lucidity + random.randint(-1, 5)
            if diff >= 0:
                dmg = max(7, p_luc // 2 + random.randint(4, 8)) + companion_bonus_dmg + total_gear_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Lucidity] You expose {npc.name}'s blind spot, exploiting their frantic breathing for {dmg} tactical damage!")
            else:
                log_lines.append(f"[Lucidity] {npc.name}'s battle instincts ignore your mind game.")

        elif action_type == "use_bandage":
            heal = 15
            self.player.current_hp = min(self.player.max_hp, self.player.current_hp + heal)
            log_lines.append(f"You catch your breath under guard, rallying your fortitude and recovering {heal} HP!")

        self.combat_state["npc_hp"] = npc.current_hp

        # Check if NPC defeated
        if npc.current_hp <= 0:
            npc.is_dead = True
            log_lines.append(f"{npc.name} collapses into the blood-slicked mud, choking on their own blood. Dead.")
            self.combat_state = None
            self.add_log("combat_end", f"{npc.name} Slain", f"You ended the life of {npc.name}. You scavenged their remaining belongings: {', '.join(npc.loot)}.")
            for itm in npc.loot:
                self.add_inventory_item(itm)
            return self.get_state()

        # NPC Counter-Attack
        enemy_roll = random.choice(["sinew", "guile", "lucidity"])
        enemy_dmg = 0
        if enemy_roll == "sinew":
            enemy_dmg = max(4, npc.stats.sinew // 3 + random.randint(2, 6))
            log_lines.append(f"{npc.name} drives a brutal crushing counter-blow, dealing {enemy_dmg} damage!")
        elif enemy_roll == "guile":
            enemy_dmg = max(5, npc.stats.guile // 3 + random.randint(3, 5))
            log_lines.append(f"{npc.name} darts forward with lethal swiftness, cutting you for {enemy_dmg} damage!")
        else:
            enemy_dmg = max(3, npc.stats.lucidity // 3 + random.randint(1, 4))
            log_lines.append(f"{npc.name} feints and strikes with cruel precision, dealing {enemy_dmg} damage!")

        self.player.current_hp = max(0, self.player.current_hp - enemy_dmg)

        if self.player.current_hp <= 0:
            self.game_over = True
            self.combat_state = None
            self.add_log("death", "You Have Perished", f"{npc.name} delivered the fatal blow. Your corpse joins the heaps of Oakhaven.")
            return self.get_state()

        self.combat_state["combat_log"] = log_lines
        self.combat_state["turn"] += 1
        return self.get_state()

    # --- Prologue Final Climax / Escape ---
    def attempt_escape(self, method: str) -> Dict[str, Any]:
        """Escape methods: 'sluice_gate' (requires Master Sluice Key), 'iron_gate' (requires Imperial Pass or Dawnshroud Seal)"""
        if method == "sluice_gate":
            if "Master Sluice Key" not in self.player.inventory:
                return {"error": "The heavy iron sluice grate is locked with three deadbolts. You require the Master Sluice Key!"}

            self.victory = True
            self.add_log(
                "victory",
                "ESCAPE THROUGH THE SMUGGLER'S SLUICE",
                (
                    "You insert the rusted master key into the triple tumblers. With a screech of tortured iron, the sluice grate yields. "
                    "You slip through the stagnant subterranean canal as the clock strikes midnight above. "
                    "Distant explosions rumble through the stone—white phosphorus cascades across Oakhaven in a brilliant, apocalyptic shower. "
                    "Behind you, the screaming dies into silence. Ahead lies the dark expanse of the Outer Barrens. "
                    "You survived the Sinking of Oakhaven. End of Prologue."
                )
            )
            return self.get_state()

        elif method == "iron_gate":
            has_pass = "Imperial Transit Pass" in self.player.inventory or "Silver Dawnshroud Seal" in self.player.inventory
            if not has_pass:
                return {"error": "The Iron Drake mercenaries and Dawnbound crossbowmen bar passage. You require a Transit Pass or Dawnshroud Seal!"}

            self.victory = True
            pass_used = "Imperial Transit Pass" if "Imperial Transit Pass" in self.player.inventory else "Silver Dawnshroud Seal"
            self.add_log(
                "victory",
                "PASSAGE THROUGH THE FLAMING GALLOW-GATE",
                (
                    f"Presenting the {pass_used}, the sentries hesitate before turning the iron winch. "
                    "The heavy timber portcullis rises just as alarm horns blare from the watchtowers. "
                    "You cross the moat into the foggy pine barrens as the first phosphorus shells burst over the chantry. "
                    "The skies burn crimson. You and your comrades breathe cold, clean night air. "
                    "You survived the Sinking of Oakhaven. End of Prologue."
                )
            )
            return self.get_state()

        return {"error": "Unknown escape method."}

    def get_save_summary(self) -> Dict[str, Any]:
        curr_loc = self.locations.get(self.player.current_location_id)
        loc_name = curr_loc.name if curr_loc else "Unknown Area"
        party_names = [self.npcs[p].name for p in self.player.party if p in self.npcs]
        return {
            "player_name": self.player.name,
            "location_id": self.player.current_location_id,
            "location_name": loc_name,
            "bell_toll": self.bell_toll,
            "party": party_names,
            "hp": self.player.current_hp,
            "max_hp": self.player.max_hp,
            "dread": self.player.dread,
            "sovereigns": self.player.sovereigns,
        }

    def save_to_dict(self) -> Dict[str, Any]:
        return {
            "version": 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "summary": self.get_save_summary(),
            "player": {
                "name": self.player.name,
                "gender": self.player.gender,
                "title": self.player.title,
                "stats": self.player.stats.to_dict(),
                "max_hp": self.player.max_hp,
                "current_hp": self.player.current_hp,
                "dread": self.player.dread,
                "sovereigns": self.player.sovereigns,
                "inventory": list(self.player.inventory),
                "current_location_id": self.player.current_location_id,
                "party": list(self.player.party),
                "romanced_npcs": list(self.player.romanced_npcs),
                "quests": dict(self.player.quests),
                "faction_reputation": dict(self.player.faction_reputation),
            },
            "locations": {
                loc_id: {
                    "items_on_ground": list(loc.items_on_ground),
                    "npc_ids": list(loc.npc_ids),
                }
                for loc_id, loc in self.locations.items()
            },
            "npcs": {
                npc_id: {
                    "current_hp": npc.current_hp,
                    "relationship": npc.relationship,
                    "is_in_party": npc.is_in_party,
                    "is_romanced": npc.is_romanced,
                    "is_dead": npc.is_dead,
                    "can_recruit": getattr(npc, "can_recruit", True),
                }
                for npc_id, npc in self.npcs.items()
            },
            "quests": {
                q_id: q.current_stage for q_id, q in self.quests.items()
            },
            "bell_toll": self.bell_toll,
            "action_count": self.action_count,
            "game_over": self.game_over,
            "victory": self.victory,
            "current_dialogue": self.current_dialogue,
            "combat_state": self.combat_state,
            "intimacy_state": self.intimacy_state,
            "logs": list(self.logs),
        }

    def load_from_dict(self, data: Dict[str, Any]) -> bool:
        if not data or "player" not in data:
            return False

        p_data = data["player"]
        self.player.name = p_data.get("name", self.player.name)
        self.player.gender = p_data.get("gender", self.player.gender)
        self.player.title = p_data.get("title", self.player.title)
        if "stats" in p_data:
            self.player.stats = Stats.from_dict(p_data["stats"])
        self.player.max_hp = p_data.get("max_hp", self.player.max_hp)
        self.player.current_hp = p_data.get("current_hp", self.player.current_hp)
        self.player.dread = p_data.get("dread", self.player.dread)
        self.player.sovereigns = p_data.get("sovereigns", self.player.sovereigns)
        self.player.inventory = list(p_data.get("inventory", []))
        self.player.current_location_id = p_data.get("current_location_id", self.player.current_location_id)
        self.player.party = list(p_data.get("party", []))
        self.player.romanced_npcs = list(p_data.get("romanced_npcs", []))
        self.player.quests = dict(p_data.get("quests", {}))
        self.player.faction_reputation = dict(p_data.get("faction_reputation", self.player.faction_reputation))

        locs_data = data.get("locations", {})
        for loc_id, l_data in locs_data.items():
            if loc_id in self.locations:
                if "items_on_ground" in l_data:
                    self.locations[loc_id].items_on_ground = list(l_data["items_on_ground"])
                if "npc_ids" in l_data:
                    self.locations[loc_id].npc_ids = list(l_data["npc_ids"])

        npcs_data = data.get("npcs", {})
        for npc_id, n_data in npcs_data.items():
            if npc_id in self.npcs:
                npc = self.npcs[npc_id]
                npc.current_hp = n_data.get("current_hp", npc.current_hp)
                npc.relationship = n_data.get("relationship", npc.relationship)
                npc.is_in_party = n_data.get("is_in_party", npc.is_in_party)
                npc.is_romanced = n_data.get("is_romanced", npc.is_romanced)
                npc.is_dead = n_data.get("is_dead", npc.is_dead)
                if "can_recruit" in n_data:
                    npc.can_recruit = n_data["can_recruit"]

        quests_data = data.get("quests", {})
        for q_id, q_stage in quests_data.items():
            if q_id in self.quests:
                self.quests[q_id].current_stage = q_stage

        self.bell_toll = data.get("bell_toll", self.bell_toll)
        self.action_count = data.get("action_count", self.action_count)
        self.game_over = data.get("game_over", self.game_over)
        self.victory = data.get("victory", self.victory)
        self.current_dialogue = data.get("current_dialogue")
        self.combat_state = data.get("combat_state")
        self.intimacy_state = data.get("intimacy_state")
        self.logs = list(data.get("logs", self.logs))
        return True

    def save_to_file(self, slot_or_path: str = "autosave") -> str:
        slot_name = slot_or_path.strip().replace(".json", "")
        saves_dir = Path("saves")
        saves_dir.mkdir(parents=True, exist_ok=True)
        file_path = saves_dir / f"{slot_name}.json"

        data = self.save_to_dict()
        data["slot"] = slot_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return str(file_path)

    def load_from_file(self, slot_or_path: str = "autosave") -> bool:
        slot_name = slot_or_path.strip().replace(".json", "")
        file_path = Path("saves") / f"{slot_name}.json"
        if not file_path.exists():
            file_path = Path(slot_or_path)
            if not file_path.exists():
                return False

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self.load_from_dict(data)

