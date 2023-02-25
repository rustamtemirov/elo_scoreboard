from flask import Flask
from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import time
import os

current_time = int(time.time())
monthly_time = current_time - (30 * 24 * 60 * 60)
weekly_time = current_time - (7 * 24 * 60 * 60)
annual_time =  current_time - (365 * 24 * 60 * 60)
end_time = current_time
api_key = os.environ.get("API_KEY")

listOfUsers = ["CaPs"]
# data structure to keep the games of the player by player name to games player relation
playedGames = {}
app = Flask(__name__)

@app.route("/tournaments")
def loadTheBoard():
    for user in listOfUsers:
        # Get summoner ID
        summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={api_key}"
        summoner_response = requests.get(summoner_url)
        
        if summoner_response.status_code == 200:
            summoner_data = summoner_response.json()
            puu_id = summoner_data["puuid"]
        else:
            print(f"Error retrieving summoner data: {summoner_response.status_code}")
            exit()
        
        # Get match history
        matches_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puu_id}/ids?startTime={annual_time}&endTime={end_time}&start=0&count=100&api_key={api_key}"
        matches_response = requests.get(matches_url)
        if matches_response.status_code == 200:
            match_data = matches_response.json()
            print(match_data)
            for match in match_data:
                match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}?api_key={api_key}"
                match_response_json = requests.get(match_url).json()
                info = match_response_json["info"]
                participants = info["participants"]
                
                for participant in participants:
                
                    if participant["summonerName"].lower() == user.lower():
                        playedGames[user] = participant
                        break
        else:
            print(f"Error retrieving match history: {matches_response.status_code}")
            exit()
    return render_template('tournaments.html')


@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

    


