"""Game Engine managing state, dialogues, romance, attack-on-sight, party mechanics, and quests."""

import random
from typing import Dict, Any, List, Optional
from game.models import Player, NPC, Location, Quest, Stats
from game.data.prologue import (
    get_prologue_locations,
    get_prologue_npcs,
    get_prologue_quests,
    get_prologue_factions,
)


class GameEngine:
    def __init__(self):
        self.player = Player()
        self.locations: Dict[str, Location] = get_prologue_locations()
        self.npcs: Dict[str, NPC] = get_prologue_npcs()
        self.quests: Dict[str, Quest] = get_prologue_quests()
        self.factions = get_prologue_factions()
        self.logs: List[Dict[str, Any]] = []
        self.current_dialogue: Optional[Dict[str, Any]] = None
        self.combat_state: Optional[Dict[str, Any]] = None
        self.game_over: bool = False
        self.victory: bool = False

        # Initialize prologue opening narrative
        self.add_log(
            "prologue",
            "PROLOGUE: ASHEN SOLSTICE - THE SINKING OF OAKHAVEN",
            (
                "You awaken with your face pressed into damp cobbles covered in greasy ash. "
                "The iron brand of the condemned throbs raw and blistering against your neck. "
                "Around you, the quarantine walls of Oakhaven loom like teeth of a blackened maw. "
                "At midnight, the Grand Inquisitor will drop the portcullis and purge the district with white phosphorus. "
                "You have only hours to navigate the squabbling factions, forge desperate alliances, seek solace in the dark, "
                "and find a way beyond the walls before the sky catches fire."
            )
        )

    def add_log(self, category: str, title: str, text: str, meta: Optional[Dict[str, Any]] = None):
        self.logs.append({
            "category": category,
            "title": title,
            "text": text,
            "meta": meta or {}
        })

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
                    "is_romanced": npc.is_romanced
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

        return {
            "player": {
                "name": self.player.name,
                "gender": self.player.gender,
                "title": self.player.title,
                "stats": self.player.stats.to_dict(),
                "hp": self.player.current_hp,
                "max_hp": self.player.max_hp,
                "dread": self.player.dread,
                "sovereigns": self.player.sovereigns,
                "inventory": self.player.inventory,
                "party": party_members,
                "romanced": self.player.romanced_npcs,
                "factions": self.player.faction_reputation
            },
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
            "logs": self.logs[-25:],
            "game_over": self.game_over,
            "victory": self.victory
        }

    def travel(self, destination_id: str) -> Dict[str, Any]:
        if self.combat_state:
            return {"error": "You cannot flee while engaged in life-or-death combat!"}

        curr_loc = self.locations.get(self.player.current_location_id)
        if not curr_loc or destination_id not in curr_loc.connected_locations:
            return {"error": "Path is obstructed or unreachable."}

        # Check special access conditions
        if destination_id == "sluice_trench" and "Master Sluice Key" not in self.player.inventory and "Imperial Transit Pass" not in self.player.inventory:
            # Allow entering sluice trench, but leaving via gate needs the key
            pass

        self.player.current_location_id = destination_id
        dest = self.locations[destination_id]
        self.current_dialogue = None

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

        # Secret discovery if Lucidity is high
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

        # Build dynamic dialogue
        node_id = npc.dialogue_root
        # Check if quest has progressed to completion stage
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
            # Fallback to root or dismiss
            self.current_dialogue = None
            return

        formatted_choices = []
        for ch in node.choices:
            # Check stat requirement visibility
            stat_met = True
            stat_text = ""
            if ch.required_stat:
                p_stat = getattr(self.player.stats, ch.required_stat, 0)
                # Party bonus
                for party_npc_id in self.player.party:
                    if party_npc_id in self.npcs:
                        p_stat += getattr(self.npcs[party_npc_id].stats, ch.required_stat, 0) // 4
                stat_met = p_stat >= ch.required_value
                stat_text = f" [{ch.required_stat.capitalize()} {ch.required_value}]"

            # Check item required
            item_met = True
            if ch.item_required and ch.item_required not in self.player.inventory:
                item_met = False

            # Check sovereigns required
            sovereigns_met = True
            if ch.sovereign_cost > 0 and self.player.sovereigns < ch.sovereign_cost:
                sovereigns_met = False

            formatted_choices.append({
                "id": ch.id,
                "text": ch.text,
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

        # Check stat requirements
        p_stat_val = 0
        if chosen_choice.required_stat:
            p_stat_val = getattr(self.player.stats, chosen_choice.required_stat, 0)
            for party_id in self.player.party:
                if party_id in self.npcs:
                    p_stat_val += getattr(self.npcs[party_id].stats, chosen_choice.required_stat, 0) // 4

            if p_stat_val < chosen_choice.required_value:
                if chosen_choice.failure_node:
                    self.load_dialogue_node(npc, chosen_choice.failure_node)
                    return self.get_state()
                else:
                    return {"error": f"Requires {chosen_choice.required_stat.capitalize()} {chosen_choice.required_value}."}

        # Check sovereign cost
        if chosen_choice.sovereign_cost > 0:
            if self.player.sovereigns < chosen_choice.sovereign_cost:
                return {"error": f"Requires {chosen_choice.sovereign_cost} Sovereigns (You have {self.player.sovereigns})."}
            self.player.sovereigns -= chosen_choice.sovereign_cost
            self.add_log("item", "Sovereigns Paid", f"You paid {chosen_choice.sovereign_cost} Sovereigns.")

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
                    # Remove required quest item if present in stages
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

        # Handle Romance Intimacy Vignette
        if chosen_choice.is_intimacy_action:
            npc.is_romanced = True
            if npc.id not in self.player.romanced_npcs:
                self.player.romanced_npcs.append(npc.id)
            # Intimacy reduces dread/sanity loss and grants passionate clarity
            self.player.dread = max(0, self.player.dread - 20)
            self.add_log(
                "romance",
                f"Solace in the Dark: {npc.name}",
                f"You shared a night of intense, carnal intimacy with {npc.name}. The creeping terror of the purge is staved off; Dread reduced by 20."
            )

        # Handle Hostility trigger
        if chosen_choice.is_hostile_action or npc.relationship <= -50:
            self.current_dialogue = None
            self.start_combat(npc.id, ambush=False)
            return self.get_state()

        # Advance node or close
        next_node_id = chosen_choice.next_node
        if next_node_id in ("vanya_recruited", "malakor_recruited"):
            self.recruit_party(npc.id)

        self.load_dialogue_node(npc, next_node_id)
        return self.get_state()

    def close_dialogue(self) -> Dict[str, Any]:
        self.current_dialogue = None
        return self.get_state()

    def recruit_party(self, npc_id: str) -> Dict[str, Any]:
        if npc_id not in self.npcs:
            return {"error": "Character not found."}
        npc = self.npcs[npc_id]

        if not npc.is_combatant:
            return {"error": f"{npc.name} is too frail or unfit for battle and cannot join the frontlines."}

        if npc.relationship < 50:
            return {"error": f"{npc.name} does not trust you enough to fight at your side (Requires 50+ Relationship, current: {npc.relationship})."}

        if npc.is_in_party:
            return {"error": f"{npc.name} is already in your party."}

        if len(self.player.party) >= 2:
            return {"error": "Party is full (maximum 2 companions)."}

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
            # Ambush first strike on player
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

        # Companion assistance
        companion_bonus_dmg = 0
        for p_id in self.player.party:
            if p_id in self.npcs:
                c = self.npcs[p_id]
                c_dmg = max(2, c.stats.sinew // 3)
                companion_bonus_dmg += c_dmg
                log_lines.append(f"{c.name} strikes with their weapon, inflicting {c_dmg} damage!")

        # Player Action Resolution
        if action_type == "sinew_strike":
            # Direct heavy blow
            diff = self.player.stats.sinew - npc.stats.sinew + random.randint(-2, 4)
            if diff >= 0:
                dmg = max(6, self.player.stats.sinew // 2 + random.randint(2, 6)) + companion_bonus_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Sinew] You overpower {npc.name}'s guard, driving iron deep into flesh for {dmg} damage!")
            else:
                dmg = max(2, random.randint(1, 3)) + companion_bonus_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Sinew] {npc.name} braces against your assault, parrying partially. You inflict {dmg} glancing damage.")

        elif action_type == "guile_skirmish":
            # Swift evasive puncture
            diff = self.player.stats.guile - npc.stats.guile + random.randint(-2, 4)
            if diff >= 0:
                dmg = max(8, int(self.player.stats.guile * 0.7) + random.randint(3, 7)) + companion_bonus_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Guile] Slipping through the shadows, your blade pierces an unarmored seam for {dmg} critical damage!")
            else:
                dmg = 3 + companion_bonus_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Guile] {npc.name} tracks your feint, deflecting your strike! You land only {dmg} scratch damage.")

        elif action_type == "lucidity_feint":
            # Tactical manipulation or blinding dust
            diff = self.player.stats.lucidity - npc.stats.lucidity + random.randint(-1, 5)
            if diff >= 0:
                dmg = max(7, self.player.stats.lucidity // 2 + random.randint(4, 8)) + companion_bonus_dmg
                npc.current_hp = max(0, npc.current_hp - dmg)
                log_lines.append(f"[Lucidity] You expose {npc.name}'s blind spot, exploiting their frantic breathing for {dmg} tactical damage!")
            else:
                log_lines.append(f"[Lucidity] {npc.name}'s sheer battle instincts ignore your mind game.")

        elif action_type == "use_bandage":
            if "Torn Bandage" in self.player.inventory or "Purified Bandage" in self.player.inventory:
                heal = 18
                if "Purified Bandage" in self.player.inventory:
                    self.player.inventory.remove("Purified Bandage")
                    heal = 25
                else:
                    self.player.inventory.remove("Torn Bandage")
                self.player.current_hp = min(self.player.max_hp, self.player.current_hp + heal)
                log_lines.append(f"You hurriedly bind your gashes, recovering {heal} HP!")
            else:
                log_lines.append("You frantically search your pouch, but have no bandages left!")

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
