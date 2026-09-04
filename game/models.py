"""Data models for the Dark, Tragic Adult Text RPG."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class Stats:
    sinew: int = 10      # Physical might, endurance, bodily resistance, intimidation
    guile: int = 10      # Reflexes, precision, agility, sleight of hand, stealth
    lucidity: int = 10   # Mental fortitude, perception, occult insight, deception reading

    def to_dict(self) -> Dict[str, int]:
        return {
            "sinew": self.sinew,
            "guile": self.guile,
            "lucidity": self.lucidity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stats":
        return cls(
            sinew=data.get("sinew", 10),
            guile=data.get("guile", 10),
            lucidity=data.get("lucidity", 10),
        )


@dataclass
class DialogueChoice:
    id: str
    text: str
    next_node: str
    required_stat: Optional[str] = None  # "sinew", "guile", "lucidity"
    required_value: int = 0
    relationship_change: int = 0
    faction_changes: Dict[str, int] = field(default_factory=dict)
    quest_trigger: Optional[str] = None
    quest_stage_set: Optional[int] = None
    item_required: Optional[str] = None
    item_reward: Optional[str] = None
    item_rewards: List[str] = field(default_factory=list)
    sovereign_cost: int = 0
    is_romance_action: bool = False
    is_intimacy_action: bool = False
    is_hostile_action: bool = False
    failure_node: Optional[str] = None


@dataclass
class DialogueNode:
    id: str
    speaker_name: str
    text: str
    choices: List[DialogueChoice] = field(default_factory=list)


@dataclass
class QuestStage:
    stage_id: int
    description: str
    target_location: Optional[str] = None
    target_npc: Optional[str] = None
    required_item: Optional[str] = None


@dataclass
class Quest:
    id: str
    title: str
    description: str
    giver_npc_id: str
    faction_id: str
    current_stage: int = 0  # 0 = not started, 1+ = active, -1 = failed, 99 = completed
    stages: Dict[int, QuestStage] = field(default_factory=dict)
    reward_items: List[str] = field(default_factory=list)
    reward_sovereigns: int = 0
    reward_relation: int = 25
    reward_faction_points: int = 20
    completion_text: str = ""


@dataclass
class NPC:
    id: str
    name: str
    title: str
    gender: str          # "female", "male", "other"
    faction_id: str
    description: str
    stats: Stats
    max_hp: int = 30
    current_hp: int = 30
    relationship: int = 0  # -100 to +100
    is_combatant: bool = True
    can_romance: bool = True
    is_in_party: bool = False
    is_romanced: bool = False
    is_dead: bool = False
    dialogue_root: str = "root"
    dialogue_nodes: Dict[str, DialogueNode] = field(default_factory=dict)
    active_quest_id: Optional[str] = None
    loot: List[str] = field(default_factory=list)


@dataclass
class Location:
    id: str
    name: str
    subtitle: str
    description: str
    faction_id: str
    connected_locations: List[str] = field(default_factory=list)
    npc_ids: List[str] = field(default_factory=list)
    items_on_ground: List[str] = field(default_factory=list)
    danger_level: int = 1


@dataclass
class Player:
    name: str = "Wanderer"
    gender: str = "male"
    title: str = "The Marked Outcast"
    stats: Stats = field(default_factory=lambda: Stats(sinew=13, guile=12, lucidity=12))
    max_hp: int = 40
    current_hp: int = 40
    dread: int = 15       # 0 (calm) to 100 (abject despair/madness)
    sovereigns: int = 25  # Currency
    inventory: List[str] = field(default_factory=lambda: ["Dulled Dirk", "Torn Bandage", "Charred Rations"])
    current_location_id: str = "gallow_square"
    party: List[str] = field(default_factory=list)  # NPC IDs in party
    romanced_npcs: List[str] = field(default_factory=list)
    quests: Dict[str, int] = field(default_factory=dict)  # quest_id -> current_stage
    faction_reputation: Dict[str, int] = field(default_factory=lambda: {
        "dawnshroud": 0,
        "iron_drakes": 0,
        "pariahs": 10
    })
