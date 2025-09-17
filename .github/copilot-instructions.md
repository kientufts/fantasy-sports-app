# Fantasy Sports Player Scoring App

This workspace contains a Python-based fantasy sports application with weighted player scoring.

## Project Overview

- **Language**: Python 3.12+
- **Framework**: Flask (web interface)
- **Database**: SQLite
- **Features**: Player management, weighted scoring, web interface

## Key Components

- `app.py`: Flask web application
- `main.py`: Console application
- `database.py`: SQLite database operations
- `scoring.py`: Weighted score calculations
- `models.py`: Player data models
- `templates/`: HTML templates

## Scoring Algorithm

Uses weighted average formula: `(Week1×1 + Week2×2 + ... + WeekN×N) ÷ (1+2+...+N)`

This prioritizes recent performance in player rankings.

## Running the Application

### Console Version
```bash
python main.py
```

### Web Version
```bash
python app.py
```
Then visit http://127.0.0.1:5000

## Development Notes

- Database auto-initializes with sample data
- Players sorted by weighted final scores
- Web interface includes leaderboard, team/position views, and detailed player analytics
- Modular design for easy customization
