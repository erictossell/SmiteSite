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
                    if (gdt[y]['god'] == mdt[x]['GodName']):
                        match_data.append([mdt[x]['taskForce'],
                                           mdt[x]['GodName'],
                                           mdt[x]['playerName'],
                                           pdt[0]['HoursPlayed'],
                                           round(gdt[y]['Wins']/(gdt[y]['Wins']+gdt[y]['Losses']),2),
                                           gdt[y]['Wins']+gdt[y]['Losses'],
                                           round(((gdt[y]['Kills']+gdt[y]['Assists'])/gdt[y]['Deaths']),2),
                                           "https://web2.hirez.com/smite/god-icons/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg"])
                        found = True
                if found == False:
                    match_data.append([mdt[x]['taskForce'],
                                           mdt[x]['GodName'],
                                           mdt[x]['playerName'],
                                           pdt[0]['HoursPlayed'],
                                           0,
                                           0,
                                           0,
                                           "https://web2.hirez.com/smite/god-icons/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg"])
                        
            else:
                match_data.append([mdt[x]['taskForce'],mdt[x]['GodName'],'','','','','',"https://web2.hirez.com/smite/god-icons/"+ mdt[x]['GodName'].lower().replace(" ","-").replace("'","") +".jpg"])
        #print("{} | {:12} | {:16} | {:5} | {:4} | {:3} | {:4}".format(" ","God","Player","Hours","Win %","Games", "KDA"))
        return match_data

def win_prediction(match_data):
        if match_data == "Offline" or match_data == "Private":
            return "No Access"
        else:
            mx = match_data
            mx = sorted(mx,key=lambda x: (x[0],x[1]))
            '''
            for z in range(len(mx)):
                if len(mx[z]) == 2:
                    print("{} | {:12} | {:16}".format(mx[z][0],mx[z][1],""))
                else:
                    print("{} | {:12} | {:16} | {:5} | {:4} | {:3} | {:4}".format(mx[z][0], mx[z][1], mx[z][2], mx[z][3], mx[z][4], mx[z][5], mx[z][6]))
            '''
            team1skill = 0
            team1hours = 0
            team1wins = 0
            count = 0
            point = len(mdt)//2
            for a in range(point):
                if mx[a][2] != '':
                    count +=1
                    team1hours += mx[a][3]
                    team1wins += mx[a][4]*mx[a][5]
            team1hours /= count
            team1wins /= count
            team2skill = 0
            team2hours = 0
            team2wins = 0
            count = 0
            for a in range(point,len(mdt)):
                if mx[a][2] != '':
                    count +=1
                    team2hours += mx[a][3]
                    team2wins += mx[a][4]*mx[a][5]
            team2hours /= count
            team2wins /= count
            team1skill = (team1hours/(team1hours + team2hours) + team1wins/(team1wins + team2wins))/2
            team2skill = 1 - team1skill
            #print("Team 1 Skill: {}%".format(round(100*team1skill,2)))
            #print("Team 2 Skill: {}%".format(round(100*team2skill,2)))
            return (team1skill, team2skill)

#gods = call('getgods', dev_id, auth_key, session_id, time, "/1")
#print(gods[0])
live = live_match_data(dev_id, auth_key, session_id, time, "EckiD")
print(live)
win = win_prediction(live)
print(win)

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
