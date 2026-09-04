import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from game.engine import GameEngine
import uuid

app = Flask(__name__)
app.secret_key = "grimdark_oakhaven_purge_secret_key"

SAVES_DIR = Path("saves")

# In-memory storage for active sessions (session_id -> GameEngine)
GAMES = {}

def get_engine() -> GameEngine:
    if "session_id" not in session or session["session_id"] not in GAMES:
        sid = str(uuid.uuid4())
        session["session_id"] = sid
        GAMES[sid] = GameEngine()
    return GAMES[session["session_id"]]

def list_saves():
    SAVES_DIR.mkdir(parents=True, exist_ok=True)
    saves = []
    for p in sorted(SAVES_DIR.glob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            slot = p.stem
            saves.append({
                "slot": slot,
                "timestamp": data.get("timestamp", ""),
                "summary": data.get("summary", {}),
                "is_autosave": (slot == "autosave"),
                "mtime": p.stat().st_mtime
            })
        except Exception:
            continue
    saves.sort(key=lambda s: s["mtime"], reverse=True)
    return saves

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state", methods=["GET"])
def api_state():
    engine = get_engine()
    return jsonify(engine.get_state())

@app.route("/api/saves", methods=["GET"])
def api_saves():
    return jsonify({"saves": list_saves()})

@app.route("/api/save", methods=["POST"])
def api_save():
    engine = get_engine()
    data = request.get_json() or {}
    slot = data.get("slot", "slot_1")
    engine.save_to_file(slot)
    return jsonify({"success": True, "slot": slot, "state": engine.get_state()})

@app.route("/api/load", methods=["POST"])
def api_load():
    engine = get_engine()
    data = request.get_json() or {}
    slot = data.get("slot", "slot_1")
    ok = engine.load_from_file(slot)
    if not ok:
        return jsonify({"error": f"Failed to load save slot: {slot}"}), 404
    return jsonify({"success": True, "slot": slot, "state": engine.get_state()})

@app.route("/api/continue", methods=["POST"])
def api_continue():
    saves = list_saves()
    if not saves:
        return jsonify({"error": "No saved game found to continue."}), 404
    latest_slot = saves[0]["slot"]
    engine = get_engine()
    ok = engine.load_from_file(latest_slot)
    if not ok:
        return jsonify({"error": f"Failed to load save: {latest_slot}"}), 404
    return jsonify({"success": True, "slot": latest_slot, "state": engine.get_state()})

@app.route("/api/action", methods=["POST"])
def api_action():
    engine = get_engine()
    data = request.get_json() or {}
    action = data.get("action")

    if action == "travel":
        dest_id = data.get("destination_id")
        res = engine.travel(dest_id)
    elif action == "inspect":
        res = engine.inspect_ground()
    elif action == "talk":
        npc_id = data.get("npc_id")
        res = engine.talk_npc(npc_id)
    elif action == "dialogue_choice":
        choice_id = data.get("choice_id")
        res = engine.choose_dialogue(choice_id)
    elif action == "close_dialogue":
        res = engine.close_dialogue()
    elif action == "recruit":
        npc_id = data.get("npc_id")
        res = engine.recruit_party(npc_id)
    elif action == "dismiss":
        npc_id = data.get("npc_id")
        res = engine.dismiss_party(npc_id)
    elif action == "combat_action":
        act_type = data.get("combat_type")
        res = engine.combat_action(act_type)
    elif action in ("start_erotic_scene", "start_intimacy"):
        npc_id = data.get("npc_id")
        res = engine.start_party_erotic_scene(npc_id)
    elif action == "intimacy_action":
        technique = data.get("technique")
        res = engine.intimacy_action(technique)
    elif action == "close_intimacy":
        res = engine.close_intimacy()
    elif action == "use_item":
        item_name = data.get("item_name")
        res = engine.use_item(item_name)
    elif action == "escape":
        method = data.get("method")
        res = engine.attempt_escape(method)
    elif action == "save":
        slot = data.get("slot", "slot_1")
        engine.save_to_file(slot)
        res = engine.get_state()
    elif action == "load":
        slot = data.get("slot", "slot_1")
        ok = engine.load_from_file(slot)
        if not ok:
            res = {"error": f"Failed to load save slot: {slot}"}
        else:
            res = engine.get_state()
    elif action == "continue":
        saves = list_saves()
        if not saves:
            res = {"error": "No saved game found to continue."}
        else:
            ok = engine.load_from_file(saves[0]["slot"])
            if not ok:
                res = {"error": f"Failed to load save: {saves[0]['slot']}"}
            else:
                res = engine.get_state()
    elif action == "reset":
        sid = session.get("session_id")
        if sid:
            GAMES[sid] = GameEngine()
        res = get_engine().get_state()
    else:
        res = {"error": f"Unknown action: {action}"}

    # Automatically update autosave on state-advancing actions
    if action in ("travel", "dialogue_choice", "combat_action", "intimacy_action", "use_item", "recruit", "dismiss"):
        try:
            engine.save_to_file("autosave")
        except Exception:
            pass

    return jsonify(res)

if __name__ == "__main__":
    print("Starting Dark Text RPG Server at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5050, debug=True)


