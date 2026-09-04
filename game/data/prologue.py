"""Prologue chapter data loader: loads structured JSON configuration files."""

import json
from pathlib import Path
from typing import Dict, Any, List

from game.models import Location, NPC, Quest, DialogueNode

DATA_DIR = Path(__file__).resolve().parent / "prologue"


def _load_json(filename: str) -> Any:
    """Load a JSON file from the prologue data directory."""
    filepath = DATA_DIR / filename
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_prologue_metadata() -> Dict[str, Any]:
    """Return prologue metadata including title, opening narrative, and intimacy locations."""
    return _load_json("metadata.json")


def get_prologue_factions() -> Dict[str, Dict[str, str]]:
    """Return prologue factions dictionary."""
    return _load_json("factions.json")


def get_prologue_locations() -> Dict[str, Location]:
    """Return prologue locations instantiated as Location models."""
    data = _load_json("locations.json")
    return {loc_id: Location.from_dict(loc_data) for loc_id, loc_data in data.items()}


def get_prologue_quests() -> Dict[str, Quest]:
    """Return prologue quests instantiated as Quest models."""
    data = _load_json("quests.json")
    return {quest_id: Quest.from_dict(quest_data) for quest_id, quest_data in data.items()}


def get_prologue_npcs() -> Dict[str, NPC]:
    """Return prologue NPCs with their dialogue trees loaded from respective JSON files."""
    npcs_data = _load_json("npcs.json")
    npcs: Dict[str, NPC] = {}
    for npc_id, npc_data in npcs_data.items():
        dialogue_file = npc_data.get("dialogue_file", f"dialogues/{npc_id}.json")
        dialogue_raw = _load_json(dialogue_file)
        dialogue_nodes = {
            node_id: DialogueNode.from_dict(node_data)
            for node_id, node_data in dialogue_raw.items()
        }
        npcs[npc_id] = NPC.from_dict(npc_data, dialogue_nodes=dialogue_nodes)
    return npcs


# Suitability mapping for intimacy scenes, maintaining full backward compatibility
SUITABLE_INTIMACY_LOCATIONS: Dict[str, List[str]] = get_prologue_metadata().get(
    "suitable_intimacy_locations", {
        "sister_vanya": ["ruined_chantry", "gilded_rat"],
        "madame_silve": ["gilded_rat", "ruined_chantry"]
    }
)
