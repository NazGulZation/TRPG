"""Prologue chapter data loader: loads structured configuration from SQLite database."""

import json
from typing import Dict, Any, List

from game.models import Location, NPC, Quest, DialogueNode, Item
from game.data.db import get_db_connection


def get_prologue_metadata() -> Dict[str, Any]:
    """Return prologue metadata including title, opening narrative, and intimacy locations from SQLite."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM metadata WHERE chapter_id = 'prologue'").fetchone()
    conn.close()
    if not row:
        return {}
    return {
        "chapter_id": row["chapter_id"],
        "title": row["title"],
        "opening_log": {
            "category": row["opening_category"],
            "title": row["opening_title"],
            "text": row["opening_text"],
        },
        "suitable_intimacy_locations": json.loads(row["suitable_intimacy_locations"] or "{}"),
    }


def get_prologue_factions() -> Dict[str, Dict[str, str]]:
    """Return prologue factions dictionary from SQLite."""
    conn = get_db_connection()
    rows = conn.execute("SELECT faction_id, name, desc, color FROM factions WHERE chapter_id = 'prologue'").fetchall()
    conn.close()
    return {
        row["faction_id"]: {
            "name": row["name"],
            "desc": row["desc"],
            "color": row["color"],
        }
        for row in rows
    }


def get_prologue_items() -> Dict[str, Item]:
    """Return prologue items instantiated as Item models, indexed by ID and Name from SQLite."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM items WHERE chapter_id = 'prologue'").fetchall()
    conn.close()

    items: Dict[str, Item] = {}
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
        # Also index by display name for flexible lookup
        items[item.name] = item
    return items


def get_prologue_locations() -> Dict[str, Location]:
    """Return prologue locations instantiated as Location models from SQLite."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM locations WHERE chapter_id = 'prologue'").fetchall()
    conn.close()

    locations: Dict[str, Location] = {}
    for row in rows:
        locations[row["location_id"]] = Location(
            id=row["location_id"],
            name=row["name"],
            subtitle=row["subtitle"] or "",
            description=row["description"] or "",
            faction_id=row["faction_id"] or "",
            connected_locations=json.loads(row["connected_locations"] or "[]"),
            npc_ids=json.loads(row["npc_ids"] or "[]"),
            items_on_ground=json.loads(row["items_on_ground"] or "[]"),
            danger_level=row["danger_level"] if row["danger_level"] is not None else 1,
        )
    return locations


def get_prologue_quests() -> Dict[str, Quest]:
    """Return prologue quests instantiated as Quest models from SQLite."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM quests WHERE chapter_id = 'prologue'").fetchall()
    conn.close()

    quests: Dict[str, Quest] = {}
    for row in rows:
        raw_stages = json.loads(row["stages"] or "{}")
        quest_data = {
            "id": row["quest_id"],
            "title": row["title"],
            "description": row["description"] or "",
            "giver_npc_id": row["giver_npc_id"] or "",
            "faction_id": row["faction_id"] or "",
            "current_stage": row["current_stage"] or 0,
            "stages": raw_stages,
            "reward_items": json.loads(row["reward_items"] or "[]"),
            "reward_sovereigns": row["reward_sovereigns"] or 0,
            "reward_relation": row["reward_relation"] if row["reward_relation"] is not None else 25,
            "reward_faction_points": row["reward_faction_points"] if row["reward_faction_points"] is not None else 20,
            "completion_text": row["completion_text"] or "",
        }
        quests[row["quest_id"]] = Quest.from_dict(quest_data)
    return quests


def get_prologue_npcs() -> Dict[str, NPC]:
    """Return prologue NPCs with their dialogue trees loaded from SQLite."""
    conn = get_db_connection()
    npc_rows = conn.execute("SELECT * FROM npcs WHERE chapter_id = 'prologue'").fetchall()
    dialogue_rows = conn.execute("SELECT * FROM dialogues WHERE chapter_id = 'prologue'").fetchall()
    conn.close()

    # Group dialogue nodes by npc_id
    dialogues_by_npc: Dict[str, Dict[str, DialogueNode]] = {}
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

    npcs: Dict[str, NPC] = {}
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


# Suitability mapping for intimacy scenes, maintaining full backward compatibility
SUITABLE_INTIMACY_LOCATIONS: Dict[str, List[str]] = get_prologue_metadata().get(
    "suitable_intimacy_locations", {
        "sister_vanya": ["ruined_chantry", "gilded_rat"],
        "madame_silve": ["gilded_rat"]
    }
)
