from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import requests
import datetime
import hashlib

#current time
t = datetime.datetime.utcnow()
time = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(t.year, t.month, t.day, t.hour, t.minute, t.second)

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

def call(api_type, dev_id, auth_key, session_id, time, parameter1, parameter2="", parameter3=""):
    call_sig = signature(dev_id, api_type, auth_key, time)
    call_string = api_url + "/" + api_type + "json/" + dev_id + "/" + call_sig + "/" + session_id + "/" + time + parameter1 + parameter2 + parameter3
    print(call_string)
    response = requests.get(call_string).json()
    return response
    
session_id = start_session(dev_id, auth_key, time)

def live_match_data(dev_id, auth_key, session_id, time, player_name):
    #Get Player Status
    player_id = call("getplayer", dev_id, auth_key, session_id, time, "/"+player_name, "", "")
    if player_id == []:
        return "Private"
    player_id = player_id[0]["Id"]
    player_id = "/" + str(player_id)
    getplayerstatus = call("getplayerstatus", dev_id, auth_key, session_id, time, player_id)
    player_status = getplayerstatus[0]["status_string"]
    if (player_status != "In Game"):
        return "Offline"
    else:
        match_id = "/" + str(getplayerstatus[0]["Match"])
        mdt = call("getmatchplayerdetails", dev_id, auth_key, session_id, time, match_id)
        match_data = []
        for x in range(len(mdt)):
            pdt = call("getplayer", dev_id, auth_key, session_id, time, "/"+mdt[x]['playerId'])
            if (mdt[x]['playerName'] != ''):
                gdt = call("getgodranks", dev_id, auth_key, session_id, time, "/"+mdt[x]['playerName'])
                found = False
                for y in range(len(gdt)):
                    if (gdt[y]['god'] == mdt[x]['GodName']):        #i will reformat this to a dictionary, I am silly. :P
                        match_data.append([mdt[x]['taskForce'],     #0
                                           mdt[x]['GodName'],       #1
                                           mdt[x]['playerName'],    #2
                                           pdt[0]['HoursPlayed'],   #3
                                           gdt[y]['Wins'],          #4
                                           gdt[y]['Wins']+gdt[y]['Losses'], #5
                                           round(((gdt[y]['Kills']+gdt[y]['Assists'])/gdt[y]['Deaths']),2), #6
                                           "/static/img/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg", #7
                                           "public"])   #8
                        found = True
                if found == False:
                    match_data.append([mdt[x]['taskForce'],
                                           mdt[x]['GodName'],
                                           mdt[x]['playerName'],
                                           pdt[0]['HoursPlayed'],
                                           0,
                                           0,
                                           0,
                                           "/static/img/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg",
                                           "public"])
            else:
                match_data.append([mdt[x]['taskForce'],mdt[x]['GodName'],'','','','','',"/static/img/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg","private"])
        #print("{} | {:12} | {:16} | {:5} | {:4} | {:3} | {:4}".format(" ","God","Player","Hours","Win %","Games", "KDA"))
        match_data = {'id':match_id,'data':match_data}
        return match_data

def pregame_data(match_data):
    team_1 = {
        'gods': [],
        'time': 0,
#        'god_wins': 0,
        'god_games': 0,
#        'god_winrate': 0,
#        'god_kda': 0,
#        'public': 0
    }
    team_2 = {
        'gods': [],
        'time': 0,
#        'god_wins': 0,
        'god_games': 0,
#        'god_winrate': 0,
#        'god_kda': 0,
#        'public': 0
    }
    
    half = len(match_data['data'])//2
    team_1_publics = 0
    team_2_publics = 0
    for p in range(0,half):
        team_1['gods'].append(match_data['data'][p][1]) #god
        if (match_data['data'][p][-1] == "public"):
            team_1['time'] += match_data['data'][p][3]      #time
            team_1['god_games'] += match_data['data'][p][5] #god_games
            team_1_publics += 1
    if (team_1['time'] != 0):
        team_1['time'] /= team_1_publics
    if (team_1['god_games'] != 0):
        team_1['god_games'] /= team_1_publics
    
    for p in range(half,len(match_data['data'])):
        team_2['gods'].append(match_data['data'][p][1]) #god
        if (match_data['data'][p][-1] == "public"):
            team_2['time'] += match_data['data'][p][3]      #time
            team_2['god_games'] += match_data['data'][p][5] #god_games
            team_2_publics += 1
    if (team_2['time'] != 0):
        team_2['time'] /= team_2_publics
    if (team_2['god_games'] != 0):
        team_2['god_games'] /= team_2_publics
    print(team_1_publics)
    print(team_2_publics)
    print(match_data['id'])
    return ({'id':match_data['id'],'teams':[team_1, team_2]})

def postgame_data(match_id):
    return call('getdemodetails', dev_id, auth_key, session_id, time, match_id)[0]['Winning_Team']

live = live_match_data(dev_id, auth_key, session_id, time, "simplicityxo")
print(live)
if live != "Offline" and live != "Private":
    pred = pregame_data(live)
    print(pred)
x = postgame_data('/942154704')
print(x)

'''
import pandas as pd
import xgboost as xjb
from sklearn.linear_model import LogisticalRegression
from sklearn.svm import SVC
from IPython.display import display

def training_add_features(data):
    None

def training_add_result(data):
    None

def win_prediction(training):
    training = pd.read_csv('final_dataset.csv')
'''



            
#gods = call('getgods', dev_id, auth_key, session_id, time, "/1")
#print(gods[0])
'''
live = live_match_data(dev_id, auth_key, session_id, time, "EckiD")
print(live)
win = win_prediction(live)
print(win)
'''
#@app.route('/player/'+name)
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search", methods=['GET'])
def search():
    if request.method=='GET':
        username=request.args.get('player')
        
        live = live_match_data(dev_id, auth_key, session_id, time, username)
        if live == "Offline": #the player is not ingame
            return "<h1>Offline</h1>"
        elif live =="Private":
            return "<h1>Private</h1>"
        else: #the player is ingame
            #return render_template("index.html")
            return render_template("main.html", data=live)
    return render_template("main.html", data=live)            
