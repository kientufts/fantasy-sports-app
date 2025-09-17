"""
Flask web application for the Fantasy Sports Player Scoring App
Multi-League Support for F1, EPL, UCL, NFL
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from database import Database
from scoring import WeightedScoreCalculator
from models import Player
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-multi-league'  # Change this in production

# Initialize database and calculator
db = Database()
calculator = WeightedScoreCalculator()

def get_current_league():
    """Get the currently selected league from session, default to EPL"""
    return session.get('current_league', 2)  # Default to EPL

def set_current_league(league_id):
    """Set the currently selected league in session"""
    session['current_league'] = league_id

@app.route('/')
@app.route('/league/<int:league_id>')
def index(league_id=None):
    """Home page showing the leaderboard for selected league"""
    if league_id:
        set_current_league(league_id)
    
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    
    if not league:
        flash('League not found, switching to EPL', 'error')
        set_current_league(2)
        return redirect(url_for('index'))
    
    # Get players for this league and calculate scores
    players = db.get_players_by_league(current_league)
    for player in players:
        player.final_score = calculator.calculate_weighted_score(player.scores)
    
    # Sort by final score in descending order
    players.sort(key=lambda p: p.final_score, reverse=True)
    
    # Get all leagues for navigation
    all_leagues = db.get_all_leagues()
    
    return render_template('index.html', 
                         players=players, 
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    """Add a new player to the currently selected league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    all_leagues = db.get_all_leagues()
    
    if request.method == 'POST':
        name = request.form['name']
        team = request.form['team']
        position = request.form['position']
        is_on_my_team = 'is_on_my_team' in request.form
        league_id = int(request.form.get('league_id', current_league))
        
        # Parse scores from form (comma-separated values)
        scores_str = request.form['scores']
        try:
            scores = [float(score.strip()) for score in scores_str.split(',')]
            player = Player(name, team, position, scores, is_on_my_team, league_id)
            
            if db.add_player(player):
                league_name = db.get_league_by_id(league_id).display_name
                team_status = " and added to your team" if is_on_my_team else ""
                flash(f'Player {name} added to {league_name} successfully!{team_status}', 'success')
                
                # Switch to the league where the player was added
                set_current_league(league_id)
                return redirect(url_for('index'))
            else:
                flash(f'Player {name} already exists in this league!', 'error')
        except ValueError:
            flash('Invalid scores format. Please enter comma-separated numbers.', 'error')
    
    return render_template('add_player.html', 
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/player/<player_name>')
def player_detail(player_name):
    """Show detailed information for a specific player"""
    current_league = get_current_league()
    player = db.get_player_by_name(player_name, current_league)
    
    if player:
        # Calculate detailed breakdown
        detailed_calc = calculator.calculate_weighted_score_detailed(player.scores)
        player.final_score = detailed_calc['final_score']
        
        all_leagues = db.get_all_leagues()
        current_league_obj = db.get_league_by_id(current_league)
        
        return render_template('player_detail.html', 
                             player=player, 
                             calculation=detailed_calc,
                             current_league=current_league_obj,
                             all_leagues=all_leagues)
    else:
        flash(f'Player {player_name} not found in current league.', 'error')
        return redirect(url_for('index'))

@app.route('/toggle_team/<player_name>')
def toggle_team_status(player_name):
    """Toggle whether a player is on my team or not"""
    success = db.toggle_my_team_status(player_name)
    if success:
        current_league = get_current_league()
        player = db.get_player_by_name(player_name, current_league)
        if player and player.is_on_my_team:
            flash(f'{player_name} added to your team!', 'success')
        elif player:
            flash(f'{player_name} removed from your team!', 'success')
    else:
        flash(f'Player {player_name} not found.', 'error')
    
    return redirect(url_for('index'))

@app.route('/my_team')
def my_team():
    """Show only players on my team in current league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    my_team_players = db.get_my_team_players(current_league)
    
    # Sort by final score
    for player in my_team_players:
        player.final_score = calculator.calculate_weighted_score(player.scores)
    my_team_players.sort(key=lambda p: p.final_score, reverse=True)
    
    all_leagues = db.get_all_leagues()
    
    return render_template('my_team.html', 
                         players=my_team_players,
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/available_players')
def available_players():
    """Show only available players (not on my team) in current league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    available = db.get_available_players(current_league)
    
    # Sort by final score
    for player in available:
        player.final_score = calculator.calculate_weighted_score(player.scores)
    available.sort(key=lambda p: p.final_score, reverse=True)
    
    all_leagues = db.get_all_leagues()
    
    return render_template('available_players.html', 
                         players=available,
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/edit_player/<player_name>', methods=['GET', 'POST'])
def edit_player(player_name):
    """Edit an existing player in current league"""
    current_league = get_current_league()
    player = db.get_player_by_name(player_name, current_league)
    
    if not player:
        flash(f'Player {player_name} not found in current league.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_name = request.form['name']
        new_team = request.form['team']
        new_position = request.form['position']
        
        # Parse scores from form (comma-separated values)
        scores_str = request.form['scores']
        try:
            new_scores = [float(score.strip()) for score in scores_str.split(',')]
            
            if db.update_player_info(player_name, new_name, new_team, new_position, new_scores):
                flash(f'Player {new_name} updated successfully!', 'success')
                return redirect(url_for('player_detail', player_name=new_name))
            else:
                flash('Failed to update player. Name might already exist.', 'error')
        except ValueError:
            flash('Invalid scores format. Please enter comma-separated numbers.', 'error')
    
    all_leagues = db.get_all_leagues()
    current_league_obj = db.get_league_by_id(current_league)
    
    return render_template('edit_player.html', 
                         player=player,
                         current_league=current_league_obj,
                         all_leagues=all_leagues)

@app.route('/delete_player/<player_name>', methods=['POST'])
def delete_player(player_name):
    """Delete a player from current league"""
    if db.delete_player(player_name):
        flash(f'Player {player_name} deleted successfully!', 'success')
    else:
        flash(f'Failed to delete player {player_name}.', 'error')
    return redirect(url_for('index'))

@app.route('/manage_data')
def manage_data():
    """Show data management page for current league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    players = db.get_players_by_league(current_league)
    all_leagues = db.get_all_leagues()
    
    return render_template('manage_data.html', 
                         players=players,
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/delete_all_players', methods=['POST'])
def delete_all_players():
    """Delete all players (with confirmation)"""
    confirmation = request.form.get('confirmation')
    if confirmation == 'DELETE ALL PLAYERS':
        deleted_count = db.delete_all_players()
        flash(f'All {deleted_count} players deleted successfully!', 'success')
    else:
        flash('Incorrect confirmation text. No players were deleted.', 'error')
    return redirect(url_for('index'))

@app.route('/api/leaderboard')
@app.route('/api/leaderboard/<int:league_id>')
def api_leaderboard(league_id=None):
    """API endpoint for leaderboard data"""
    if not league_id:
        league_id = get_current_league()
    
    players = db.get_players_by_league(league_id)
    for player in players:
        player.final_score = calculator.calculate_weighted_score(player.scores)
    players.sort(key=lambda p: p.final_score, reverse=True)
    
    return jsonify([player.to_dict() for player in players])

@app.route('/teams')
def teams():
    """Show players grouped by teams in current league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    all_players = db.get_players_by_league(current_league)
    teams_dict = {}
    
    for player in all_players:
        player.final_score = calculator.calculate_weighted_score(player.scores)
        if player.team not in teams_dict:
            teams_dict[player.team] = []
        teams_dict[player.team].append(player)
    
    # Sort players within each team by final score
    for team in teams_dict:
        teams_dict[team].sort(key=lambda p: p.final_score, reverse=True)
    
    all_leagues = db.get_all_leagues()
    
    return render_template('teams.html', 
                         teams=teams_dict,
                         current_league=league,
                         all_leagues=all_leagues)

@app.route('/positions')
def positions():
    """Show players grouped by positions in current league"""
    current_league = get_current_league()
    league = db.get_league_by_id(current_league)
    all_players = db.get_players_by_league(current_league)
    positions_dict = {}
    
    for player in all_players:
        player.final_score = calculator.calculate_weighted_score(player.scores)
        if player.position not in positions_dict:
            positions_dict[player.position] = []
        positions_dict[player.position].append(player)
    
    # Sort players within each position by final score
    for position in positions_dict:
        positions_dict[position].sort(key=lambda p: p.final_score, reverse=True)
    
    all_leagues = db.get_all_leagues()
    
    return render_template('positions.html', 
                         positions=positions_dict,
                         current_league=league,
                         all_leagues=all_leagues)

# League Management Routes
@app.route('/switch_league/<int:league_id>')
def switch_league(league_id):
    """Switch to a different league"""
    league = db.get_league_by_id(league_id)
    if league:
        session['current_league'] = league_id
        flash(f'Switched to {league.display_name} ({league.sport_type})', 'success')
    else:
        flash('League not found!', 'error')
    return redirect(url_for('index'))

@app.route('/leagues')
def leagues_overview():
    """Show overview of all leagues"""
    leagues = db.get_all_leagues()
    league_stats = []
    
    for league in leagues:
        players = db.get_players_by_league(league.id)
        my_team_count = len([p for p in players if p.is_on_my_team])
        league_stats.append({
            'league': league,
            'total_players': len(players),
            'my_team_players': my_team_count
        })
    
    return render_template('leagues.html', league_stats=league_stats)

if __name__ == '__main__':
    # Initialize sample data if needed
    all_leagues = db.get_all_leagues()
    for league in all_leagues:
        if len(db.get_players_by_league(league.id)) == 0:
            # If any league is empty, run the populate script
            import populate_leagues
            populate_leagues.populate_all_leagues()
            break
    
    app.run(debug=True, port=5000)
