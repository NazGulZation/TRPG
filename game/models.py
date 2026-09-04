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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DialogueChoice":
        return cls(
            id=data["id"],
            text=data["text"],
            next_node=data["next_node"],
            required_stat=data.get("required_stat"),
            required_value=data.get("required_value", 0),
            relationship_change=data.get("relationship_change", 0),
            faction_changes=data.get("faction_changes") or {},
            quest_trigger=data.get("quest_trigger"),
            quest_stage_set=data.get("quest_stage_set"),
            item_required=data.get("item_required"),
            item_reward=data.get("item_reward"),
            item_rewards=data.get("item_rewards") or [],
            sovereign_cost=data.get("sovereign_cost", 0),
            is_romance_action=data.get("is_romance_action", False),
            is_intimacy_action=data.get("is_intimacy_action", False),
            is_hostile_action=data.get("is_hostile_action", False),
            failure_node=data.get("failure_node"),
        )


@dataclass
class DialogueNode:
    id: str
    speaker_name: str
    text: str
    choices: List[DialogueChoice] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DialogueNode":
        choices = [
            c if isinstance(c, DialogueChoice) else DialogueChoice.from_dict(c)
            for c in data.get("choices", [])
        ]
        return cls(
            id=data["id"],
            speaker_name=data["speaker_name"],
            text=data["text"],
            choices=choices,
        )


@dataclass
class QuestStage:
    stage_id: int
    description: str
    target_location: Optional[str] = None
    target_npc: Optional[str] = None
    required_item: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuestStage":
        return cls(
            stage_id=int(data["stage_id"]),
            description=data["description"],
            target_location=data.get("target_location"),
            target_npc=data.get("target_npc"),
            required_item=data.get("required_item"),
        )


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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quest":
        raw_stages = data.get("stages", {})
        stages = {}
        for sid, sdata in raw_stages.items():
            stage_obj = sdata if isinstance(sdata, QuestStage) else QuestStage.from_dict(sdata)
            stages[int(sid)] = stage_obj
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            giver_npc_id=data["giver_npc_id"],
            faction_id=data["faction_id"],
            current_stage=data.get("current_stage", 0),
            stages=stages,
            reward_items=data.get("reward_items") or [],
            reward_sovereigns=data.get("reward_sovereigns", 0),
            reward_relation=data.get("reward_relation", 25),
            reward_faction_points=data.get("reward_faction_points", 20),
            completion_text=data.get("completion_text", ""),
        )


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
    can_recruit: bool = True
    is_in_party: bool = False
    is_romanced: bool = False
    is_dead: bool = False
    dialogue_root: str = "root"
    dialogue_nodes: Dict[str, DialogueNode] = field(default_factory=dict)
    active_quest_id: Optional[str] = None
    loot: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], dialogue_nodes: Optional[Dict[str, DialogueNode]] = None) -> "NPC":
        raw_stats = data.get("stats", {})
        stats = raw_stats if isinstance(raw_stats, Stats) else Stats.from_dict(raw_stats)

        nodes = dialogue_nodes if dialogue_nodes is not None else {}
        if not nodes and "dialogue_nodes" in data:
            nodes = {
                nid: nd if isinstance(nd, DialogueNode) else DialogueNode.from_dict(nd)
                for nid, nd in data["dialogue_nodes"].items()
            }

        return cls(
            id=data["id"],
            name=data["name"],
            title=data.get("title", ""),
            gender=data.get("gender", "other"),
            faction_id=data.get("faction_id", ""),
            description=data.get("description", ""),
            stats=stats,
            max_hp=data.get("max_hp", 30),
            current_hp=data.get("current_hp", 30),
            relationship=data.get("relationship", 0),
            is_combatant=data.get("is_combatant", True),
            can_romance=data.get("can_romance", True),
            can_recruit=data.get("can_recruit", True),
            is_in_party=data.get("is_in_party", False),
            is_romanced=data.get("is_romanced", False),
            is_dead=data.get("is_dead", False),
            dialogue_root=data.get("dialogue_root", "root"),
            dialogue_nodes=nodes,
            active_quest_id=data.get("active_quest_id"),
            loot=data.get("loot") or [],
        )


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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Location":
        return cls(
            id=data["id"],
            name=data["name"],
            subtitle=data.get("subtitle", ""),
            description=data.get("description", ""),
            faction_id=data.get("faction_id", ""),
            connected_locations=data.get("connected_locations") or [],
            npc_ids=data.get("npc_ids") or [],
            items_on_ground=data.get("items_on_ground") or [],
            danger_level=data.get("danger_level", 1),
        )


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
