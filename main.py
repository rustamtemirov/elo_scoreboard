from flask import Flask
import requests
from datetime import datetime, timedelta

api_key = "RGAPI-12d69e71-76d6-47ee-b511-abe2eb50a5af"
summoner_name = "CaPs"

# Get summoner ID
summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
summoner_response = requests.get(summoner_url)

if summoner_response.status_code == 200:
    summoner_data = summoner_response.json()
    summoner_id = summoner_data["id"]
    account_id = summoner_data["accountId"]
else:
    print(f"Error retrieving summoner data: {summoner_response.status_code}")
    exit()

# Get match history
match_url = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key={api_key}"
match_response = requests.get(match_url)

if match_response.status_code == 200:
    match_data = match_response.json()
    thirty_days_ago = datetime.now() - timedelta(days=30)
    last_thirty_days_matches = [match for match in match_data["matches"] if datetime.fromtimestamp(match["timestamp"]/1000) > thirty_days_ago]
    print(f"Last 30 days matches for {summoner_name}:")
    for match in last_thirty_days_matches:
        print(f"Match ID: {match['gameId']}, Champion: {match['champion']}")
else:
    print(f"Error retrieving match history: {match_response.status_code}")
    exit()


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, LOLboard!'