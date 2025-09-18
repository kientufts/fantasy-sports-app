# Fantasy Sports App - Project Structure

```
fantasy/
├── launcher.py                 # Quick launcher (calls main launcher)
├── main.py                     # Console application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── src/                        # Source code
│   ├── core/                   # Core business logic
│   │   ├── database.py         # Database operations
│   │   ├── models.py           # Data models (Player, League)
│   │   └── scoring.py          # Scoring algorithms
│   │
│   └── web/                    # Web application
│       ├── app.py              # Flask web app
│       └── templates/          # HTML templates
│           ├── index.html
│           ├── my_team.html
│           ├── available_players.html
│           ├── add_player.html
│           ├── edit_player.html
│           ├── player_detail.html
│           ├── positions.html
│           ├── teams.html
│           ├── leagues.html
│           └── manage_data.html
│
├── scripts/                    # Utility scripts
│   ├── status_checker.py       # App status monitoring
│   │
│   ├── launchers/              # Application launchers
│   │   ├── launcher.py         # Main cross-platform launcher
│   │   ├── start_app.bat       # Windows quick start
│   │   ├── start_app.sh        # Linux/macOS quick start
│   │   ├── start_web_app.bat   # Windows web app launcher
│   │   ├── launch.bat          # Legacy Windows launcher
│   │   └── launch.sh           # Legacy Unix launcher
│   │
│   └── setup/                  # Database setup and migration
│       ├── migrate_db.py       # Original database migration
│       ├── migrate_multi_league.py  # Multi-league migration
│       ├── populate_leagues.py # Sample data population
│       ├── setup-git.bat       # Git setup (Windows)
│       └── setup-git.sh        # Git setup (Unix)
│
├── data/                       # Data storage
│   └── fantasy_players.db      # SQLite database
│
├── docs/                       # Documentation
│   └── GIT_SETUP_COMPLETE.md   # Git setup confirmation
│
└── .vscode/                    # VS Code configuration
    └── tasks.json              # VS Code tasks
```

## Quick Start Commands

### Any OS (Recommended)
```bash
python launcher.py
```

### Windows
```cmd
scripts\launchers\start_app.bat
```

### Linux/macOS  
```bash
chmod +x scripts/launchers/start_app.sh
./scripts/launchers/start_app.sh
```

## File Organization

- **Root Level**: Essential files (launcher, main app, requirements)
- **src/core/**: Core business logic and data handling
- **src/web/**: Web interface and templates  
- **scripts/launchers/**: All startup scripts and launchers
- **scripts/setup/**: Database migration and setup tools
- **data/**: Database and data files
- **docs/**: Documentation and guides

This structure provides clear separation of concerns and makes the project easy to navigate and maintain.
