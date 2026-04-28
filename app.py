from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from wumpus_environment import WumpusWorld
from knowledge_base import KnowledgeBase
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Store game states
games = {}

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/new_game', methods=['POST'])
def new_game():
    try:
        data = request.json
        rows = int(data.get('rows', 4))
        cols = int(data.get('cols', 4))
        num_pits = int(data.get('num_pits', 2))
        
        game_id = str(len(games))
        world = WumpusWorld(rows, cols, num_pits)
        kb = KnowledgeBase(rows, cols)
        
        games[game_id] = {
            'world': world,
            'kb': kb,
            'agent_pos': (0, 0),
            'visited': set([(0, 0)]),
            'inference_steps': 0,
            'game_over': False,
            'won': False,
            'agent_alive': True
        }
        
        # Add initial position to visited
        world.agent_visited.add((0, 0))
        
        # Get initial percepts
        initial_percepts = world.get_percepts(0, 0)
        
        return jsonify({
            'game_id': game_id,
            'grid': world.get_visible_grid(),
            'dimensions': {'rows': rows, 'cols': cols},
            'agent_pos': [0, 0],
            'percepts': initial_percepts,
            'inference_steps': 0,
            'kb_size': len(kb.clauses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/move', methods=['POST'])
def move_agent():
    try:
        data = request.json
        game_id = data['game_id']
        direction = data['direction']
        
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        game = games[game_id]
        world = game['world']
        kb = game['kb']
        
        if game['game_over']:
            return jsonify({'error': 'Game is over'}), 400
        
        # Calculate new position
        x, y = game['agent_pos']
        new_pos = list(game['agent_pos'])
        
        if direction == 'up' and x > 0:
            new_pos[0] -= 1
        elif direction == 'down' and x < world.rows - 1:
            new_pos[0] += 1
        elif direction == 'left' and y > 0:
            new_pos[1] -= 1
        elif direction == 'right' and y < world.cols - 1:
            new_pos[1] += 1
        else:
            return jsonify({'error': 'Invalid move'}), 400
        
        new_pos = tuple(new_pos)
        game['agent_pos'] = new_pos
        game['visited'].add(new_pos)
        world.agent_visited.add(new_pos)
        
        # Get percepts at new position
        percepts = world.get_percepts(new_pos[0], new_pos[1])
        
        # Check for hazards
        cell = world.grid[new_pos[0]][new_pos[1]]
        
        if cell['pit']:
            game['game_over'] = True
            game['agent_alive'] = False
            return jsonify({
                'game_over': True,
                'won': False,
                'message': 'Agent fell into a pit! Game Over!',
                'percepts': percepts,
                'grid': world.get_visible_grid(),
                'full_grid': world.get_full_grid(),
                'agent_pos': [new_pos[0], new_pos[1]]
            })
        
        if cell['wumpus']:
            game['game_over'] = True
            game['agent_alive'] = False
            return jsonify({
                'game_over': True,
                'won': False,
                'message': 'Agent was eaten by the Wumpus! Game Over!',
                'percepts': percepts,
                'grid': world.get_visible_grid(),
                'full_grid': world.get_full_grid(),
                'agent_pos': [new_pos[0], new_pos[1]]
            })
        
        # Check if gold is found
        if cell['gold']:
            game['game_over'] = True
            game['won'] = True
            return jsonify({
                'game_over': True,
                'won': True,
                'message': 'Congratulations! Agent found the gold! You Win!',
                'percepts': percepts,
                'grid': world.get_visible_grid(),
                'full_grid': world.get_full_grid(),
                'agent_pos': [new_pos[0], new_pos[1]]
            })
        
        # Update knowledge base with percepts
        kb.tell_percepts(new_pos[0], new_pos[1], percepts)
        
        return jsonify({
            'game_over': False,
            'won': False,
            'new_position': [new_pos[0], new_pos[1]],
            'percepts': percepts,
            'grid': world.get_visible_grid(),
            'inference_steps': game.get('inference_steps', 0),
            'kb_size': len(kb.clauses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_safe_cells', methods=['POST'])
def get_safe_cells():
    try:
        data = request.json
        game_id = data['game_id']
        
        if game_id not in games:
            return jsonify({'error': 'Game not found'}), 404
        
        game = games[game_id]
        kb = game['kb']
        world = game['world']
        agent_pos = game['agent_pos']
        
        # Get adjacent cells
        x, y = agent_pos
        adjacent = []
        if x > 0: adjacent.append([x-1, y])
        if x < world.rows - 1: adjacent.append([x+1, y])
        if y > 0: adjacent.append([x, y-1])
        if y < world.cols - 1: adjacent.append([x, y+1])
        
        # Check which cells are safe using resolution
        safe_cells = []
        inference_steps = 0
        
        for cell in adjacent:
            if tuple(cell) not in game['visited']:
                # Query KB about this cell
                result, steps = kb.query_safety(cell[0], cell[1])
                inference_steps += steps
                if result:
                    safe_cells.append(cell)
        
        game['inference_steps'] = game.get('inference_steps', 0) + inference_steps
        
        return jsonify({
            'safe_cells': safe_cells,
            'inference_steps': game['inference_steps'],
            'kb_size': len(kb.clauses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500