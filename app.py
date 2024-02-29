
from configs import *
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from python_funcs.players import *
from python_funcs.livedata import *
from python_funcs.sql_helper import *
from python_funcs.teams import *

import os
os.environ['FLASK_DEBUG'] = '1'


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    scoreboard = get_today_scoreboard()
    standings = get_standings()
    print('data loaded')
    return jsonify({
        'upcomingGames': scoreboard.to_dict(orient='records'),
        'standings': standings.to_dict(orient='records')
    })

@app.route('/standings/')
def standings():
    league_data = get_league_stats()
    return render_template('standings.html', league_data=league_data)

@app.route('/player/<int:player_id>/<metric>')
def player(player_id, metric):
    player_name = get_player_name_by_id(player_id)
    player_list = get_player_stats(player_id)
    metric_title = player_stats_dict[metric]
    return render_template(
        'player.html',
        player_name=player_name,
        player_data=player_list.to_dict(orient='records'),
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
        conn = get_db_connection('players')
        players = conn.execute('SELECT full_name FROM players order by full_name asc').fetchall()
        metrics = player_stats_dict.items()
        conn.close()
        return render_template('select.html', players=players, metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)
