import sqlite3
import json
from configs import *
from nba_api.stats.endpoints import playercareerstats
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from werkzeug.exceptions import abort

import os
os.environ['FLASK_DEBUG'] = '1'

def get_db_connection():
    conn = sqlite3.connect('players.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_player_by_id(player_id):
    conn = get_db_connection()
    player = conn.execute('SELECT * FROM players WHERE id = ?',
                        (player_id,)).fetchone()
    conn.close()
    return player

def get_player_id_by_name(full_name):
    conn = get_db_connection()
    player_id = conn.execute('SELECT id FROM players WHERE full_name = ?',
                        (full_name,)).fetchone()[0]
    conn.close()
    return player_id

def get_player_name_by_id(player_id):
    conn = get_db_connection()
    player_name = conn.execute('SELECT full_name FROM players WHERE id = ?',
                        (player_id,)).fetchone()[0]
    conn.close()
    return player_name

def get_player_stats_as_list(player_id):
    player_dict = json.loads(playercareerstats.PlayerCareerStats(player_id).get_json())['resultSets'][0]
    player_stats_list = []
    for row in player_dict['rowSet']:
        player_stats_list.append({player_dict['headers'][i]: row[i] for i in range(len(row))})
    return player_stats_list


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player/<int:player_id>/<metric>')
def player(player_id, metric):
    player_name = get_player_name_by_id(player_id)
    player_list = get_player_stats_as_list(player_id)
    metric_title = player_stats_dict[metric]
    return render_template(
        'player.html',
        player_name=player_name,
        player_data=player_list,
        metric=metric,
        metric_title=metric_title)

@app.route('/select/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        player_name = request.form["player"]
        metric = request.form["metric"]
        player_id = get_player_id_by_name(player_name)
        return redirect(url_for("player",player_id=player_id, metric=metric))
    else:
        conn = get_db_connection()
        players = conn.execute('SELECT full_name FROM players order by full_name asc').fetchall()
        metrics = player_stats_dict.items()
        conn.close()
        return render_template('select.html', players=players, metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)
