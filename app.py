from flask import Flask, render_template, request, session, redirect, url_for
from game_data import GameData
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

game_data = GameData()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    # Initialize game state if new session
    if 'current_scene' not in session:
        session['current_scene'] = 'prologue_start'
        session['choices_made'] = []
        session['inventory'] = []
        session['stats'] = {
            'hope': 50,
            'guilt': 50,
            'resolve': 50
        }
    
    scene_id = session['current_scene']
    scene = game_data.get_scene(scene_id)
    
    if scene is None:
        return redirect(url_for('index'))
    
    return render_template('game.html', 
                         scene=scene,
                         stats=session.get('stats', {}),
                         inventory=session.get('inventory', []))

@app.route('/choose', methods=['POST'])
def choose():
    choice_index = int(request.form.get('choice', 0))
    current_scene_id = session.get('current_scene', 'prologue_start')
    
    # Get the next scene based on choice
    next_scene_id = game_data.get_next_scene(current_scene_id, choice_index)
    
    # Record the choice
    if 'choices_made' not in session:
        session['choices_made'] = []
    session['choices_made'].append({
        'scene': current_scene_id,
        'choice': choice_index
    })
    
    # Update stats based on choice
    stat_changes = game_data.get_stat_changes(current_scene_id, choice_index)
    if 'stats' not in session:
        session['stats'] = {'hope': 50, 'guilt': 50, 'resolve': 50}
    
    for stat, change in stat_changes.items():
        session['stats'][stat] = max(0, min(100, session['stats'][stat] + change))
    
    # Add items if any
    items_gained = game_data.get_items_gained(current_scene_id, choice_index)
    if items_gained:
        if 'inventory' not in session:
            session['inventory'] = []
        session['inventory'].extend(items_gained)
    
    session['current_scene'] = next_scene_id
    session.modified = True
    
    return redirect(url_for('game'))

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
