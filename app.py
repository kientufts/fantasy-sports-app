"""
Flask web application for the Fantasy Sports Player Scoring App
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from main import FantasyApp
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
fantasy_app = FantasyApp()

@app.route('/')
def index():
    """Home page showing the leaderboard"""
    leaderboard = fantasy_app.get_leaderboard()
    return render_template('index.html', players=leaderboard)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    """Add a new player"""
    if request.method == 'POST':
        name = request.form['name']
        team = request.form['team']
        position = request.form['position']
        is_on_my_team = 'is_on_my_team' in request.form
        
        # Parse scores from form (comma-separated values)
        scores_str = request.form['scores']
        try:
            scores = [float(score.strip()) for score in scores_str.split(',')]
            fantasy_app.add_player(name, team, position, scores, is_on_my_team)
            
            team_status = " and added to your team" if is_on_my_team else ""
            flash(f'Player {name} added successfully!{team_status}', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid scores format. Please enter comma-separated numbers.', 'error')
    
    return render_template('add_player.html')

@app.route('/player/<player_name>')
def player_detail(player_name):
    """Show detailed information for a specific player"""
    player = fantasy_app.db.get_player_by_name(player_name)
    if player:
        # Calculate detailed breakdown
        detailed_calc = fantasy_app.calculator.calculate_weighted_score_detailed(player.scores)
        player.final_score = detailed_calc['final_score']
        return render_template('player_detail.html', player=player, calculation=detailed_calc)
    else:
        flash(f'Player {player_name} not found.', 'error')
        return redirect(url_for('index'))

@app.route('/toggle_team/<player_name>')
def toggle_team_status(player_name):
    """Toggle whether a player is on my team or not"""
    success = fantasy_app.db.toggle_my_team_status(player_name)
    if success:
        player = fantasy_app.db.get_player_by_name(player_name)
        if player and player.is_on_my_team:
            flash(f'{player_name} added to your team!', 'success')
        elif player:
            flash(f'{player_name} removed from your team!', 'success')
    else:
        flash(f'Player {player_name} not found.', 'error')
    
    return redirect(url_for('index'))

@app.route('/my_team')
def my_team():
    """Show only players on my team"""
    my_team_players = fantasy_app.db.get_my_team_players()
    # Sort by final score
    for player in my_team_players:
        player.final_score = fantasy_app.calculator.calculate_weighted_score(player.scores)
    my_team_players.sort(key=lambda p: p.final_score, reverse=True)
    
    return render_template('my_team.html', players=my_team_players)

@app.route('/available_players')
def available_players():
    """Show only available players (not on my team)"""
    available = fantasy_app.db.get_available_players()
    # Sort by final score
    for player in available:
        player.final_score = fantasy_app.calculator.calculate_weighted_score(player.scores)
    available.sort(key=lambda p: p.final_score, reverse=True)
    
    return render_template('available_players.html', players=available)

@app.route('/edit_player/<player_name>', methods=['GET', 'POST'])
def edit_player(player_name):
    """Edit an existing player"""
    player = fantasy_app.db.get_player_by_name(player_name)
    if not player:
        flash(f'Player {player_name} not found.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_name = request.form['name']
        new_team = request.form['team']
        new_position = request.form['position']
        
        # Parse scores from form (comma-separated values)
        scores_str = request.form['scores']
        try:
            new_scores = [float(score.strip()) for score in scores_str.split(',')]
            
            if fantasy_app.db.update_player_info(player_name, new_name, new_team, new_position, new_scores):
                flash(f'Player {new_name} updated successfully!', 'success')
                return redirect(url_for('player_detail', player_name=new_name))
            else:
                flash('Failed to update player. Name might already exist.', 'error')
        except ValueError:
            flash('Invalid scores format. Please enter comma-separated numbers.', 'error')
    
    return render_template('edit_player.html', player=player)

@app.route('/delete_player/<player_name>', methods=['POST'])
def delete_player(player_name):
    """Delete a player"""
    if fantasy_app.db.delete_player(player_name):
        flash(f'Player {player_name} deleted successfully!', 'success')
    else:
        flash(f'Failed to delete player {player_name}.', 'error')
    return redirect(url_for('index'))

@app.route('/manage_data')
def manage_data():
    """Show data management page"""
    players = fantasy_app.db.get_all_players()
    return render_template('manage_data.html', players=players)

@app.route('/delete_all_players', methods=['POST'])
def delete_all_players():
    """Delete all players (with confirmation)"""
    confirmation = request.form.get('confirmation')
    if confirmation == 'DELETE ALL PLAYERS':
        deleted_count = fantasy_app.db.delete_all_players()
        flash(f'All {deleted_count} players deleted successfully!', 'success')
    else:
        flash('Incorrect confirmation text. No players were deleted.', 'error')
    return redirect(url_for('index'))

@app.route('/api/leaderboard')
def api_leaderboard():
    """API endpoint for leaderboard data"""
    leaderboard = fantasy_app.get_leaderboard()
    return jsonify([player.to_dict() for player in leaderboard])

@app.route('/teams')
def teams():
    """Show players grouped by teams"""
    all_players = fantasy_app.db.get_all_players()
    teams_dict = {}
    
    for player in all_players:
        player.final_score = fantasy_app.calculator.calculate_weighted_score(player.scores)
        if player.team not in teams_dict:
            teams_dict[player.team] = []
        teams_dict[player.team].append(player)
    
    # Sort players within each team by final score
    for team in teams_dict:
        teams_dict[team].sort(key=lambda p: p.final_score, reverse=True)
    
    return render_template('teams.html', teams=teams_dict)

@app.route('/positions')
def positions():
    """Show players grouped by positions"""
    all_players = fantasy_app.db.get_all_players()
    positions_dict = {}
    
    for player in all_players:
        player.final_score = fantasy_app.calculator.calculate_weighted_score(player.scores)
        if player.position not in positions_dict:
            positions_dict[player.position] = []
        positions_dict[player.position].append(player)
    
    # Sort players within each position by final score
    for position in positions_dict:
        positions_dict[position].sort(key=lambda p: p.final_score, reverse=True)
    
    return render_template('positions.html', positions=positions_dict)

if __name__ == '__main__':
    # Initialize with sample data if database is empty
    if not fantasy_app.db.get_all_players():
        fantasy_app.initialize_sample_data()
    
    app.run(debug=True, port=5000)
