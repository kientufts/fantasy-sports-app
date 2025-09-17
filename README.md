# Multi-League Fantasy Sports Player Scoring App

A comprehensive Python application for managing fantasy sports players across multiple leagues (Formula 1, EPL, UCL, NFL) with sophisticated weighted scoring system that prioritizes recent performance.

## Features

- **Multi-League Support**: Manage fantasy teams across Formula 1, English Premier League, UEFA Champions League, and NFL
- **League-Specific Data**: Each league has its own teams, positions, and player database
- **Session-Based League Switching**: Seamlessly switch between leagues while maintaining your progress
- **Player Database**: Store and manage hundreds of player records with team, position, and performance data
- **Weighted Scoring**: Advanced algorithm that calculates player scores using weighted averages, giving more importance to recent game weeks
- **Team Management**: Build and manage your fantasy team with visual indicators and separate views per league
- **Sortable Leaderboard**: Players automatically ranked by their final weighted scores within each league
- **Web Interface**: User-friendly Flask web application with multi-league navigation
- **Console Interface**: Interactive command-line interface with league switching and team management
- **Database Filtering**: View players by teams and positions within each league
- **My Team vs Available**: Clear differentiation between rostered players and available options per league
- **Detailed Analytics**: Individual player breakdowns showing score calculations

## Supported Leagues

### Formula 1 (Motorsport)
- **Positions**: Driver, Constructor
- **Teams**: Red Bull Racing, Mercedes, Ferrari, McLaren, Alpine, Aston Martin, Williams, AlphaTauri, Alfa Romeo, Haas

### English Premier League (Football) 
- **Positions**: Forward, Midfielder, Defender, Goalkeeper
- **Teams**: Manchester City, Arsenal, Liverpool, Chelsea, Newcastle United, Manchester United, Tottenham, Brighton, Aston Villa, West Ham

### UEFA Champions League (Football)
- **Positions**: Forward, Midfielder, Defender, Goalkeeper  
- **Teams**: Real Madrid, Manchester City, Bayern Munich, PSG, Liverpool, Barcelona, Chelsea, Inter Milan, AC Milan, Atletico Madrid

### National Football League (American Football)
- **Positions**: Quarterback, Running Back, Wide Receiver, Tight End, Defense, Kicker
- **Teams**: Kansas City Chiefs, Buffalo Bills, Cincinnati Bengals, Philadelphia Eagles, San Francisco 49ers, Dallas Cowboys, Miami Dolphins, Baltimore Ravens

## Scoring Formula

The app uses a weighted average formula that emphasizes recent performance:

```
Final Score = (Week1×1 + Week2×2 + ... + WeekN×N) ÷ (1+2+...+N)
```

This ensures that a player's most recent games have the highest impact on their final ranking, reflecting their current form within each league.

## Project Structure

```
fantasy/
├── app.py              # Flask multi-league web application
├── main.py             # Multi-league console application
├── launcher.py         # Cross-platform launcher script
├── status_checker.py   # App status checker and manager
├── launch.bat          # Windows launcher script
├── launch.sh           # macOS/Linux launcher script
├── models.py           # Player and League data models
├── database.py         # SQLite database operations with multi-league support
├── scoring.py          # Weighted score calculation logic
├── migrate_multi_league.py # Multi-league database migration script
├── populate_leagues.py # Sample data population for all leagues
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates for multi-league web interface
│   ├── index.html      # Main leaderboard with league selector
│   ├── leagues.html    # League overview and switching interface
│   ├── add_player.html # Add new player form with league-specific options
│   ├── edit_player.html # Edit existing player
│   ├── player_detail.html # Individual player details
│   ├── my_team.html    # Players on your fantasy team per league
│   ├── available_players.html # Available players in current league
│   ├── teams.html      # Players grouped by teams in current league
│   ├── positions.html  # Players grouped by positions in current league
│   └── manage_data.html # Data management interface per league
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher (Python 3.12+ recommended)
- pip (Python package installer)

### Cross-Platform Setup

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   # OR download and extract the ZIP file
   ```

2. **Navigate to the project directory**
   ```bash
   cd fantasy
   ```

3. **Install Python dependencies:**
   
   **On Windows:**
   ```cmd
   pip install -r requirements.txt
   ```
   
   **On macOS/Linux:**
   ```bash
   pip3 install -r requirements.txt
   # OR if pip points to Python 3:
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python --version    # Should show Python 3.8+
   pip list            # Should show flask, pandas, flask-sqlalchemy
   ```

## Usage

### Quick Start (Recommended)

The easiest way to run the app on any platform is using the provided launcher scripts:

**Cross-Platform Python Launcher:**
```bash
python launcher.py
# OR on some systems:
python3 launcher.py
```

**Platform-Specific Scripts:**

**Windows:**
```cmd
launch.bat
```

**macOS/Linux:**
```bash
chmod +x launch.sh
./launch.sh
```

These launchers will:
- Check your Python version
- Install dependencies automatically  
- Provide a menu to choose console or web app
- Handle platform-specific differences

### Multi-League Console Interface

Run the interactive console version to manage all your fantasy leagues:

**Interactive Mode (Recommended):**
```bash
python main.py --interactive
```

This provides a menu-driven interface where you can:
- View all available leagues (F1, EPL, UCL, NFL)
- Switch between leagues seamlessly
- View league-specific leaderboards
- Manage your team for each league
- Add players with league-specific teams and positions

**Basic Demo Mode:**
```bash
python main.py
```

Shows a quick overview of leagues and sample data.

### Manual Launch

### Console Application

Run the console version to see a simple leaderboard:

**On Windows:**
```cmd
python main.py
```

**On macOS/Linux:**
```bash
python3 main.py
# OR if python points to Python 3:
python main.py
```

This will:
- Initialize the database with sample data
- Display the current leaderboard
- Add a sample player
- Show the updated leaderboard

### Web Application

Start the Flask web server:

**On Windows:**
```cmd
python app.py
```

**On macOS/Linux:**
```bash
python3 app.py
# OR if python points to Python 3:
python app.py
```

Then open your browser to `http://127.0.0.1:5000` or `http://localhost:5000`

### Multi-League Web Interface

The web application supports seamless switching between multiple fantasy leagues:

**🏟️ League Navigation:**
- **League Selector**: Each page shows the current league and provides quick links to switch
- **Leagues Overview** (`/leagues`): Comprehensive view of all leagues with statistics
- **Session Persistence**: Your current league selection is maintained throughout your session
- **League-Specific Data**: All pages automatically filter to show only current league data

**🏎️ Formula 1 Features:**
- Driver and Constructor positions
- F1-specific teams (Red Bull Racing, Mercedes, Ferrari, etc.)
- Motorsport scoring optimized for race weekends

**⚽ Football Leagues (EPL/UCL):**
- Traditional football positions (Forward, Midfielder, Defender, Goalkeeper)
- League-specific teams and player rosters
- Match week scoring system

**🏈 NFL Features:**
- American football positions (QB, RB, WR, TE, Defense, Kicker)
- NFL teams and season-based scoring
- Fantasy football optimized calculations

#### Alternative Launch Methods:

**Using Flask's built-in command (all platforms):**
```bash
flask --app app run
# OR with debug mode:
flask --app app run --debug
```

**Using Python module execution (all platforms):**
```bash
python -m flask --app app run
# OR on macOS/Linux:
python3 -m flask --app app run
```

#### Multi-League Web Features:

- **Leaderboard** (`/`): View all players ranked by weighted score within current league with league switcher
- **Leagues Overview** (`/leagues`): Switch between leagues and see team statistics for each
- **Add Player** (`/add_player`): Add new players with league-specific team and position options
- **My Team** (`/my_team`): View only players currently on your fantasy team for current league
- **Available Players** (`/available_players`): Browse players not on your team in current league
- **Player Details** (`/player/<name>`): Detailed breakdown with league context and calculation details
- **Edit Player** (`/edit_player/<name>`): Modify existing player information within their league
- **Teams** (`/teams`): View players grouped by their teams in current league
- **Positions** (`/positions`): View players grouped by their positions in current league
- **Manage Data** (`/manage_data`): League-specific data management with bulk operations
- **API** (`/api/leaderboard`): JSON endpoint with optional league parameter

#### Team Management (Per League):

- **➕ Add to Team**: Click the green ➕ button to add a player to your fantasy team
- **➖ Remove from Team**: Click the red ➖ button to remove a player from your team
- **⭐ Team Indicators**: Stars show which players are currently on your team
- **Separate Views**: Use "My Team" to focus on your roster, "Available" to browse options
- **Color Coding**: Green buttons for My Team page, blue for Available Players page

## Database

The app uses **SQLite** for local data storage, which provides **persistent data storage** between sessions.

### Data Persistence

**✅ YES - Your data is automatically saved!**

- **Database File**: `fantasy_players.db` (created automatically in the app directory)
- **Persistent Storage**: All player data, scores, teams, and positions are saved permanently
- **Cross-Session**: Data remains intact when you close and reopen the app
- **Offline Support**: No internet connection required after initial setup

### Database Features

- **Automatic Creation**: Database and tables are created automatically on first run
- **SQLite Format**: Lightweight, file-based database (no server required)
- **ACID Compliance**: Data integrity guaranteed with proper transaction handling
- **Concurrent Access**: Multiple app instances can safely read the same database

### Database Schema

The database file contains a `players` table with the following structure:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Auto-incrementing primary key |
| `name` | TEXT | Player name (unique) |
| `team` | TEXT | Team name |
| `position` | TEXT | Player position |
| `scores` | TEXT | JSON array of game scores |
| `final_score` | REAL | Calculated weighted score |
| `is_on_my_team` | BOOLEAN | Whether player is on your fantasy team (0/1) |

### Database Migration

If you're upgrading from an older version, the app includes automatic database migration:

```bash
python migrate_db.py
```

This script will:
- Check if the `is_on_my_team` column exists
- Add the column if missing (defaults to 0/False for existing players)
- Preserve all existing data
- Enable team management features

### Data Lifecycle

1. **First Launch**: 
   - Database file is created
   - Sample data is inserted (if database is empty)
   - Players are stored permanently

2. **Subsequent Launches**:
   - Existing database is loaded
   - All previous data is preserved
   - New players can be added
   - Existing players can be updated

3. **Data Location**:
   - **File**: `fantasy_players.db` in the app directory
   - **Backup**: Copy this file to backup your data
   - **Migration**: Move this file to transfer data to another location

### Sample Data Behavior

The app includes sample players that are added **only once**:
- Sample data is inserted only if the database is empty
- On subsequent launches, sample data insertion is skipped
- Your added players persist alongside the original sample data

### Practical Examples

**Scenario 1: First Time Launch**
```bash
python launcher.py
# → Creates fantasy_players.db
# → Adds 5 sample players (John Smith, Sarah Johnson, etc.)
# → Shows leaderboard with sample data
```

**Scenario 2: Second Launch (Offline)**
```bash
python launcher.py
# → Loads existing fantasy_players.db
# → Shows same players from previous session
# → No sample data re-insertion
# → All your custom players are still there
```

**Scenario 3: Adding New Players**
```bash
# Add player via web interface or console
# → Player is permanently saved to database
# → Available in all future sessions
# → Survives app restarts, computer reboots, etc.
```

**Scenario 4: Data Backup/Transfer**
```bash
# Copy fantasy_players.db to backup location
# Move fantasy_players.db to new computer
# → All data transfers with the file
```

## Sample Data

The application comes with sample data including:

- **Players**: John Smith, Sarah Johnson, Mike Davis, Emily Wilson, Chris Brown
- **Teams**: Team A, Team B, Team C
- **Positions**: Forward, Midfielder, Defender, Goalkeeper
- **Scores**: 5 game weeks of sample performance data

## VS Code Tasks

Pre-configured tasks are available in VS Code:

- **Run Fantasy App (Console)**: Execute the console version
- **Run Fantasy App (Web)**: Start the web server

Access these via Terminal → Run Task in VS Code.

## API Usage

### Get Leaderboard Data

```bash
curl http://127.0.0.1:5000/api/leaderboard
```

Returns JSON array of all players with their calculated scores.

## Customization

### Adding New Players

**Via Web Interface:**
1. Navigate to "Add Player" page
2. Fill in player details and comma-separated scores
3. Submit the form

**Via Code:**
```python
from main import FantasyApp

app = FantasyApp()
app.add_player("Player Name", "Team", "Position", [85, 90, 78, 88, 95])
```

### Editing Player Data

**Via Web Interface:**
1. From the **Leaderboard**: Click the ✏️ edit icon next to any player
2. From **Player Detail** page: Click the "Edit Player" button
3. From **Manage Data** page: Click the "Edit" button in the Actions column
4. Modify any information (name, team, position, scores)
5. Click "Save Changes"

**Important Notes:**
- Editing a player's name will update all references
- Score changes automatically recalculate the weighted average
- All changes are saved immediately to the database

### Deleting Players

**Individual Player Deletion:**
1. From **Leaderboard**: Click the 🗑️ delete icon (with confirmation)
2. From **Player Detail** page: Click "Delete Player" button
3. From **Manage Data** page: Click "Delete" button
4. Confirm the deletion in the popup dialog

**Bulk Deletion (Remove All Players):**
1. Go to **Manage Data** page
2. Scroll to the "Danger Zone" section
3. Type "DELETE ALL PLAYERS" in the confirmation field
4. Click "Delete All Players" button
5. Confirm in the popup dialog

**⚠️ Important:** All deletions are **permanent** and cannot be undone!

### Modifying Scoring Algorithm

Edit the `WeightedScoreCalculator` class in `scoring.py` to implement different weighting schemes.

## Dependencies

- **Flask 2.3.2**: Web framework
- **Flask-SQLAlchemy 3.0.5**: Database ORM (optional, using raw SQLite)
- **Python 3.12+**: Core runtime

## Development

The application is designed with modularity in mind:

- `models.py`: Data structures
- `database.py`: Data persistence
- `scoring.py`: Business logic
- `app.py`: Web interface
- `main.py`: Console interface

## Troubleshooting

### Checking if the Web App is Running

Sometimes you may access the web interface and find it's not responding. Here are several ways to check if the Flask app is running:

#### Method 1: Use the Status Checker Script (Recommended)
```bash
python status_checker.py
```
This interactive script will:
- Check if the app is running and responding
- Show the process ID if running
- Provide options to start/stop the app
- Open the app in your browser

#### Method 2: Check Port Usage (Windows)
```cmd
netstat -ano | findstr :5000
```
- If you see output with "LISTENING", the app is running
- The PID (Process ID) will be shown in the last column
- If no output, the app is not running

#### Method 3: Check Port Usage (macOS/Linux)
```bash
lsof -i :5000
# OR
netstat -tlnp | grep :5000
```

#### Method 4: Test HTTP Response
```bash
curl http://127.0.0.1:5000
# OR open in browser: http://localhost:5000
```
- If you get HTML content, the app is running
- If connection refused/timeout, the app is not running

#### Method 5: Check Running Python Processes
**Windows:**
```cmd
tasklist | findstr python
```

**macOS/Linux:**
```bash
ps aux | grep python
ps aux | grep app.py
```

### Starting/Restarting the Web App

#### Quick Start
```bash
# Navigate to project directory
cd "path/to/fantasy"

# Start the web app
python app.py
```

#### Background Process (Keeps Running)
**Windows (PowerShell):**
```powershell
# Start as background job
Start-Job -ScriptBlock { python app.py }

# Check job status
Get-Job

# Stop job
Get-Job | Stop-Job
```

**Windows (Command Prompt):**
```cmd
# Start minimized (stays running when you close terminal)
start /min python app.py
```

**macOS/Linux:**
```bash
# Start in background
nohup python3 app.py &

# Check if running
jobs
ps aux | grep app.py

# Kill background process
pkill -f app.py
```

### Keeping the App Running Permanently

#### Option 1: VS Code Task (Recommended)
1. In VS Code, go to `Terminal → Run Task`
2. Select "Run Fantasy App (Web)"
3. The task runs in the background and shows status in VS Code terminal
4. To stop: Click the trash can icon in the terminal

#### Option 2: Windows Service (Advanced)
Create a Windows service using tools like NSSM (Non-Sucking Service Manager):
```cmd
# Install NSSM from https://nssm.cc/
nssm install FantasyApp "C:\path\to\python.exe" "C:\path\to\fantasy\app.py"
nssm start FantasyApp
```

#### Option 3: Screen/Tmux (Linux/macOS)
```bash
# Using screen
screen -S fantasy
python3 app.py
# Press Ctrl+A then D to detach

# Reattach later
screen -r fantasy

# Using tmux
tmux new -s fantasy
python3 app.py
# Press Ctrl+B then D to detach

# Reattach later
tmux attach -t fantasy
```

### Auto-Start on System Boot

#### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task → "Fantasy Sports App"
3. Trigger: "When the computer starts"
4. Action: "Start a program"
5. Program: `C:\path\to\python.exe`
6. Arguments: `C:\path\to\fantasy\app.py`
7. Start in: `C:\path\to\fantasy`

#### macOS (launchd)
Create file `~/Library/LaunchAgents/com.fantasy.app.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fantasy.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/fantasy/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```
Then: `launchctl load ~/Library/LaunchAgents/com.fantasy.app.plist`

#### Linux (systemd)
Create file `/etc/systemd/system/fantasy-app.service`:
```ini
[Unit]
Description=Fantasy Sports App
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/fantasy
ExecStart=/usr/bin/python3 /path/to/fantasy/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Then:
```bash
sudo systemctl enable fantasy-app.service
sudo systemctl start fantasy-app.service
```

### Common Issues and Solutions

#### Python Command Not Found
**Problem:** `python: command not found` or `python3: command not found`

**Solutions:**
- **Windows**: Install Python from [python.org](https://python.org) and ensure "Add Python to PATH" is checked
- **macOS**: Install Python using Homebrew: `brew install python3`
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-pip`
- **Linux (CentOS/RHEL)**: `sudo yum install python3 python3-pip`

#### Module Not Found Errors
**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solutions:**
```bash
# Ensure you're using the correct pip
pip --version      # Should match your Python version

# Install dependencies
pip install -r requirements.txt

# If you have multiple Python versions:
python3 -m pip install -r requirements.txt
```

#### Port Already in Use
**Problem:** `OSError: [Errno 48] Address already in use`

**Solutions:**
```bash
# Kill process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill
# OR use a different port:
python app.py
# Then modify app.py to use app.run(port=5001)
```

#### Database Permission Issues
**Problem:** Database file cannot be created or accessed

**Solutions:**
```bash
# Ensure write permissions in the directory
chmod 755 .                    # On macOS/Linux
# OR run from user's home directory
# OR specify a different database path in the code
```

#### Reset Database
**Problem:** Want to start fresh with clean data

**Solutions:**
```bash
# Delete the database file (loses all data!)
rm fantasy_players.db          # macOS/Linux
del fantasy_players.db         # Windows

# OR rename to keep as backup
mv fantasy_players.db fantasy_players_backup.db    # macOS/Linux
ren fantasy_players.db fantasy_players_backup.db   # Windows
```

#### Database File Missing
**Problem:** `fantasy_players.db` file accidentally deleted

**Solutions:**
- App will automatically recreate the database on next launch
- Sample data will be re-inserted
- Custom players will be lost (unless you have a backup)
- **Prevention**: Regularly backup your `fantasy_players.db` file

#### Flask Debug Mode Issues
**Problem:** Auto-reload not working or debugger issues

**Solutions:**
```bash
# Set environment variables (cross-platform)
export FLASK_ENV=development    # macOS/Linux
set FLASK_ENV=development       # Windows CMD
$env:FLASK_ENV="development"    # Windows PowerShell

# OR modify app.py directly:
app.run(debug=True, port=5000)
```

### Platform-Specific Notes

#### Windows
- Use `python` command (usually points to Python 3)
- Use Command Prompt or PowerShell
- Antivirus software may interfere with database file creation

#### macOS
- May need to use `python3` command explicitly
- Use Terminal application
- Xcode Command Line Tools may be required: `xcode-select --install`

#### Linux
- Usually requires `python3` command
- May need to install additional packages: `sudo apt install python3-dev`
- SELinux may affect file permissions on some distributions

### Virtual Environment (Recommended)

To avoid dependency conflicts, use a virtual environment:

**Create and activate:**
```bash
# Windows
python -m venv fantasy_env
fantasy_env\Scripts\activate

# macOS/Linux
python3 -m venv fantasy_env
source fantasy_env/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Deactivate when done:**
```bash
deactivate
```

## Future Enhancements

- Player photo uploads
- Export functionality (CSV, Excel)
- Advanced statistics and charts
- Multi-league support
- User authentication
- Mobile-responsive design improvements

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please check the code comments or modify the application to suit your specific fantasy sports requirements.
