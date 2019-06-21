from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import requests
import datetime
import hashlib

#current time
t = datetime.datetime.utcnow()
time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(t.year, t.month, t.day, t.hour, t.minute, t.second)
#print(time)
api_url = "http://api.smitegame.com/smiteapi.svc"
dev_id = "3222"
auth_key = "8C9376AF7E8A49A2A774574F48ED4D3F"

def signature(dev_id, api_type, auth_key, time):
    signature_string = dev_id + api_type + auth_key + time
    return hashlib.md5(signature_string.encode('utf-8')).hexdigest()

def start_session(dev_id, auth_key, time):
    session_sig = signature(dev_id, "createsession", auth_key, time)
    session_string = api_url + "/createsessionjson/" + dev_id + "/" + session_sig + "/" + time
    return requests.get(session_string).json()['session_id']

def call(api_type, dev_id, auth_key, session_id, time, parameter1, parameter2="", parameter3="", parameter4=""):
    call_sig = signature(dev_id, api_type, auth_key, time)
    call_string = api_url + "/" + api_type + "json/" + dev_id + "/" + call_sig + "/" + session_id + "/" + time + parameter1 + parameter2 + parameter3 + parameter4
    #print(call_string)
    response = requests.get(call_string).json()
    return response
    
session_id = start_session(dev_id, auth_key, time)

def player_id_from_name(dev_id, auth_key, session_id, time, player_name):
    player_id = call("getplayer", dev_id, auth_key, session_id, time, "/"+player_name, "", "")
    if player_id == []:
        return "Private"
    else:
        player_id = player_id[0]["Id"]
        player_id = "/" + str(player_id)
        return player_id
    
def player_live_data_from_id(dev_id, auth_key, session_id, time, player_id):
    player_live = call("getplayerstatus", dev_id, auth_key, session_id, time, player_id)
    return player_live

def match_data_from_match_id(dev_id, auth_key, session_id, time, match_id):
    match_data = call("getmatchplayerdetails", dev_id, auth_key, session_id, time, match_id)
    match_data = sorted(match_data, key=lambda k: k['taskForce']) 
    return match_data

def match_id_batch(dev_id, auth_key, session_id, time, queue_id, date, hour, minute):
    match_id_batch = call('getmatchidsbyqueue', dev_id, auth_key, session_id, time, queue_id, date, hour, minute)
    return match_id_batch

def god_data_from_player_id(dev_id, auth_key, session_id, time, player_id, god_id):
    god_data = call("getgodranks", dev_id, auth_key, session_id, time, "/"+player_id)
    for g in range(len(god_data)):
        if god_data[g]['god_id'] == god_id:
            #print("!!",player_id,god_id,god_data[g])
            return god_data[g]
    return False
    #print(god_data)

def player_stats_from_match_data(dev_id, auth_key, session_id, time, match_data):
    player_stats = {"taskForce1":{"player1":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player2":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player3":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player4":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player5":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0}
                                  },
                    "taskForce2":{"player6":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player7":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player8":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player9":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0},
                                  "player10":{"id":"", "hours":0, "godWins":0, "godKDA":0, "godGames":0}
                                  }}
    count = 1
    for p in range(len(match_data)):
        if match_data[p]["playerId"] == "0":
            None
        else:
            team = "taskForce1"
            if p > 4:
                team = "taskForce2"
            player_stats[team]["player"+str(count)]["id"] = match_data[p]["playerName"]
            player_hours = call("getplayer", dev_id, auth_key, session_id, time, "/"+match_data[p]['playerId'])[0]["HoursPlayed"]
            #print(match_data[p]['playerId'])
            player_stats[team]["player"+str(count)]["hours"] = player_hours
            god_data = god_data_from_player_id(dev_id, auth_key, session_id, time, match_data[p]["playerId"], str(match_data[p]["GodId"]))
            if god_data == False:
                None
            else:
                god_wins = god_data["Wins"]
                player_stats[team]["player"+str(count)]["godWins"] = god_wins
                if god_data["Deaths"] == 0:
                    god_kda = round(god_data["Kills"] + god_data["Assists"],3)
                else:
                    god_kda = round((god_data["Kills"] + god_data["Assists"]) / god_data["Deaths"],3)
                player_stats[team]["player"+str(count)]["godKDA"] = god_kda
                god_games= god_data["Wins"] + god_data["Losses"]
                player_stats[team]["player"+str(count)]["godGames"] = god_games
        count += 1
    return player_stats

def team_stats_from_player_stats(player_stats):
    team_1_hours = 0
    team_1_wins = 0
    team_1_KDA_total = 0
    team_1_KDA_weighted = 0
    team_1_games = 0
    team_1_publics = 0

    team_2_hours = 0
    team_2_wins = 0
    team_2_KDA_total = 0
    team_2_KDA_weighted = 0
    team_2_games = 0
    team_2_publics = 0
    
    for p in range(len(player_stats['taskForce1'])):
        player = player_stats['taskForce1']["player"+str(p+1)]
        if player['hours'] > 0:
            team_1_hours += player['hours']
            team_1_wins += player['godWins']
            team_1_KDA_total += (player['godKDA'] * player['godGames'])
            team_1_games += player['godGames']
            team_1_publics += 1
    if team_1_games > 0:
        team_1_KDA_weighted = round(team_1_KDA_total / team_1_games,3)
    for p in range(len(player_stats['taskForce2'])):
        player = player_stats['taskForce2']["player"+str(p+6)]
        if player['hours'] > 0:
            team_2_hours += player['hours']
            team_2_wins += player['godWins']
            team_2_KDA_total += (player['godKDA'] * player['godGames'])
            team_2_games += player['godGames']
            team_2_publics += 1
    if team_2_games > 0:
        team_2_KDA_weighted = round(team_2_KDA_total / team_2_games,3)

    if team_1_publics > 0:
        team_1_hours /= team_1_publics
        team_1_wins /= team_1_publics
    if team_2_publics > 0:
        team_2_hours /= team_2_publics
        team_2_wins /= team_2_publics
    return [team_1_hours,team_1_wins,team_1_KDA_weighted, team_2_hours,team_2_wins,team_2_KDA_weighted]
    
def run_player_stats(dev_id, auth_key, session_id, time, t):
    #print(time)

    if (t.minute//10*10-10 < 0):
        hour = "/{:02d}".format(t.hour)    
        minute = ",{:02d}".format(0)
    else:
        hour = "/{:02d}".format(t.hour)    
        minute = ",{:02d}".format(t.minute//10*10-10)
    date = "/{:04d}{:02d}{:02d}".format(t.year, t.month, t.day)
    batch_ids = match_id_batch(dev_id, auth_key, session_id, time, "/435", date, hour, minute)
    #print(batch_ids)
    match_id_x = ""
    all_data = []
    m = len(batch_ids)-1
    while m >= 0:
        if batch_ids[m]["Active_Flag"] == 'y':
            ta = 0
            #print(batch_ids[m]["Match"])
            match_id_x = batch_ids[m]["Match"]
            #print(match_id_x)
            match_data = match_data_from_match_id(dev_id, auth_key, session_id, time, "/"+match_id_x)
            #print(match_data)
            player_stats = player_stats_from_match_data(dev_id, auth_key, session_id, time, match_data)
            #print(player_stats)
            team_stats = team_stats_from_player_stats(player_stats)
            #print(team_stats)
            if team_stats[0] == 0 and team_stats[1] == 0 and team_stats[2] == 0 and team_stats[3] == 0 and team_stats[4] == 0 and team_stats[5] == 0 and ta < 3:
                if m < len(batch_ids)-1:
                    m+= 1
                    ta + 1
                print ("redo")
            else:
                all_data.append([match_id_x, team_stats[0], team_stats[1], team_stats[2], team_stats[3], team_stats[4], team_stats[5]])
                m-= 1
            print([match_id_x, team_stats[0], team_stats[1], team_stats[2], team_stats[3], team_stats[4], team_stats[5]])
        else:
            m-=1
    for x in range(len(all_data)):
        print(all_data[x])
    return all_data

datax = run_player_stats(dev_id, auth_key, session_id, time, t)
print(datax)
