"""Flask Web Server for the Dark, Tragic Adult Text RPG."""

from flask import Flask, render_template, request, jsonify, session
from game.engine import GameEngine
import uuid

app = Flask(__name__)
app.secret_key = "grimdark_oakhaven_purge_secret_key"

# In-memory storage for active sessions (session_id -> GameEngine)
GAMES = {}

def get_engine() -> GameEngine:
    if "session_id" not in session or session["session_id"] not in GAMES:
        sid = str(uuid.uuid4())
        session["session_id"] = sid
        GAMES[sid] = GameEngine()
    return GAMES[session["session_id"]]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state", methods=["GET"])
def api_state():
    engine = get_engine()
    return jsonify(engine.get_state())

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
    elif action == "reset":
        sid = session.get("session_id")
        if sid:
            GAMES[sid] = GameEngine()
        res = get_engine().get_state()
    else:
        res = {"error": f"Unknown action: {action}"}

    return jsonify(res)

if __name__ == "__main__":
    print("Starting Dark Text RPG Server at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5050, debug=True)

