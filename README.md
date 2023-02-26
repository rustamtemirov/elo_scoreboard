# Elo Scoreboard for League of Legends
This Flask app uses the Riot Games API to fetch data of a player's games and analyze their performance in order to provide ratings. The ratings are used to create two features: a leaderboard and a matching system for finding teammates or enemies with matching ratings.

## Getting started
1. Install Python 3.7+ and Flask (pip install Flask)
2. Clone the repository to your local machine
3. Get an API key from the Riot Games Developer Portal and insert it into `app.py`'s `api_key` variable
4. Run `python3 -m flask run` in your terminal
5. Open your web browser and go to `http://localhost:5000/`

## Usage
1. Select the desired time period (weekly, monthly, or annual).
2. The player's games will be analyzed, and a rating will be provided for each game. The 10 games with the highest ratings will be used to calculate an average rating for the player.
3. The player's rating will be added to the leaderboard, which can be viewed right after choosing.
4. To find a teammate or enemy with a matching rating, click the "Enemy finder" button in the navigation bar and select whether you want to find a teammate or enemy from the list of offered users.

## API reference
This app uses the Riot Games API to fetch data of a player's games. The API endpoints are accessed using the requests library.
