from flask import Flask
from flask import Flask, render_template, redirect, url_for
import requests
from datetime import datetime, timedelta
import time
import os

current_time = int(time.time())
monthly_time = current_time - (30 * 24 * 60 * 60)
weekly_time = current_time - (7 * 24 * 60 * 60)
annual_time =  current_time - (365 * 24 * 60 * 60)
end_time = current_time
api_key = "RGAPI-6d872b59-b070-4ca4-be26-f6fb08b69435"

listOfUsers = ["CaPs", "Dmlkdd", "adsMMM", "lvoDF", "ds2CC"]
# data structure to keep the games of the player by player name to games player relation

app = Flask(__name__)

@app.route("/tournament")
def tournament():
    userData = []
    for user in listOfUsers:
        playedGames = []
        # Get summoner ID
        summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={api_key}"
        summoner_response = requests.get(summoner_url)
        
        if summoner_response.status_code == 200:
            summoner_data = summoner_response.json()
            puu_id = summoner_data["puuid"]
            summoner_level = summoner_data["summonerLevel"]
        else:
            print(f"Error retrieving summoner data: {summoner_response.status_code}")
            exit()
        
        # Get match history
        matches_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puu_id}/ids?startTime={annual_time}&endTime={end_time}&start=0&count=100&api_key={api_key}"
        matches_response = requests.get(matches_url)
        if matches_response.status_code == 200:
            match_data = matches_response.json()
            
            for match in match_data:
                match_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match}?api_key={api_key}"
                match_response_json = requests.get(match_url).json()
                info = match_response_json["info"]
                participants = info["participants"]
                
                for participant in participants:
                
                    if participant["summonerName"].lower() == user.lower():
                        win =False
                        if participant["win"] == "true":
                            win = True
                        S = 0.35*win + int(participant["kills"])*0.2+ int(participant["deaths"])*0.1 + int(participant["assists"])*0.1+int(participant["physicalDamageDealt"])*0.15 + int(participant["totalHeal"])*0.1
                        playedGames.append(S)
                        break
                total =0
                playedGames.sort(reverse=True)
                arrSize = 0
                
                if len(playedGames) < 10:
                    arrSize = len(playedGames)
                else:
                    arrSize = 10

                for i in range(arrSize):
                    total += playedGames[i]
                
                total = total/arrSize

        else:
            print(f"Error retrieving match history: {matches_response.status_code}")
            exit()
        
        userDict = {}
        userDict["name"] = user
        userDict["rating"] = total
        userDict["level"] = summoner_level
        userData.append(userDict)

    return render_template('tournaments.html', users=userData)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tournaments')
def tournaments():  
    return render_template('tournaments.html')

@app.route('/enemy_finder')
def enemy_finder():
    return render_template('enemy_finder.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
    
    


