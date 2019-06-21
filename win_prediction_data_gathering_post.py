#the list of match ids
ids_list = [944106141,944106140,944106139,944106137,944106136,944106135,944106134,944106133,944106132,944106131,944106130,944106129,944106128,944106127,944106126,944106125,944106124,944106123,944106122,944106121,944106120,944106119,944106118,944106117,944106116,944106115,944106114,944106113,944106112,944106111,944106110,944106109,944106108,944106107,944106106,944106105,944106104,944106103,944106102,944106101,944106100,944106099,944106098,944106097,944106096,944106095,944106094,944106093,944106092,944106091,944106090,944106089,944106088,944106087,944106086,944106085,944105781,944105780,944105779,944105777,944105776,944105775,944105774,944105773,944105772,944105771,944105770,944105769,944105768,944105767,944105766,944105765,944105577,944105576,944105575,944105574,944105573,944105572,944105571,944105570,944105569,944105568,944105567,944105566,944105565,944105564,944105563,944105562,944105561,944105560,944105559,944105558,944105557,944105556,944105555,944105554,944105553,944105552,944105551,944105550,944105549,944105548,944105547,944105546,944105545,944105544,944105543,944105542,944105541,944105540,944105539,944105538,944105537,944105536,944105535,944106141,944106140,944106139,944106137,944106136,944106135,944106134,944106133,944106132,944106131,944106130,944106129,944106128,944106127,944106126,944106125,944106124,944106123,944106122,944106121,944106120,944106119,944106118,944106117,944106116,944106115,944106114,944106113,944106112,944106111,944106110,944106109,944106108,944106107,944106106,944106105,944106104,944106103,944106102,944106101,944106100,944106099,944106098,944106097,944106096,944106095,944106094,944106093,944106092,944106091,944106090,944106089,944106088,944106087,944106086,944106085,944105781,944105780,944105779,944105777,944105776,944105775,944105774,944105773,944105772,944105771,944105770,944105769,944105768,944105767,944105766,944105765,944105577,944105576,944105575,944105574,944105573,944105572,944105571,944105570,944105569,944105568,944105567,944105566,944105565,944105564,944105563,944105562,944105561,944105560,944105559,944105558,944105557,944105556,944105555,944105554,944105553,944105552,944105551,944105550,944105549,944105548,944105547,944105546,944105545,944105544,944105543,944105542,944105541,944105540,944105539,944105538,944105537,944105536,944105535]

import pyrez
dev_id=3222
auth_key='8C9376AF7E8A49A2A774574F48ED4D3F'
smite = pyrez.SmiteAPI(dev_id, auth_key)

#Winning_TaskForce HERE
match_results = []

#the function that returns match result from match id using getmatchdetails
def get_result_from_match_id(match_id):
    result = smite.getMatch(match_id)
    if result:
        try:
           return result[0]['Winning_TaskForce']
        except Exception:
            pass
    return -1

#loop that calls function and appends result to list
if not match_results:
    for game in ids_list:
        print(get_result_from_match_id(game))
        match_results.append(get_result_from_match_id(game))

    #for id_ in ids_list:
    #n += 1
    #ids.append(id_)
    #if n >= 5:
        #n = 0
        #ids = []
#print(match_results)

for x in match_results:
    print(x)
    
#JSON Example
"""
{
  "Account_Level": 129,
  "ActiveId1": 14146,
  "ActiveId2": 14154,
  "ActiveId3": 0,
  "ActiveId4": 0,
  "ActivePlayerId": "0",
  "Assists": 13,
  "Ban1": "",
  "Ban10": "",
  "Ban10Id": 0,
  "Ban1Id": 0,
  "Ban2": "",
  "Ban2Id": 0,
  "Ban3": "",
  "Ban3Id": 0,
  "Ban4": "",
  "Ban4Id": 0,
  "Ban5": "",
  "Ban5Id": 0,
  "Ban6": "",
  "Ban6Id": 0,
  "Ban7": "",
  "Ban7Id": 0,
  "Ban8": "",
  "Ban8Id": 0,
  "Ban9": "",
  "Ban9Id": 0,
  "Camps_Cleared": 4,
  "Conquest_Losses": 0,
  "Conquest_Points": 0,
  "Conquest_Tier": 0,
  "Conquest_Wins": 0,
  "Damage_Bot": 28509,
  "Damage_Done_In_Hand": 4828,
  "Damage_Done_Magical": 71084,
  "Damage_Done_Physical": 0,
  "Damage_Mitigated": 4845,
  "Damage_Player": 42575,
  "Damage_Taken": 18099,
  "Damage_Taken_Magical": 11704,
  "Damage_Taken_Physical": 6395,
  "Deaths": 5,
  "Distance_Traveled": 288553,
  "Duel_Losses": 0,
  "Duel_Points": 0,
  "Duel_Tier": 0,
  "Duel_Wins": 0,
  "Entry_Datetime": "6/18/2019 7:09:08 PM",
  "Final_Match_Level": 20,
  "First_Ban_Side": "",
  "GodId": 1672,
  "Gold_Earned": 17695,
  "Gold_Per_Minute": 1096,
  "Healing": 0,
  "Healing_Bot": 0,
  "Healing_Player_Self": 3155,
  "ItemId1": 8551,
  "ItemId2": 9633,
  "ItemId3": 14766,
  "ItemId4": 8354,
  "ItemId5": 7784,
  "ItemId6": 12670,
  "Item_Active_1": "Purification Beads Upgrade",
  "Item_Active_2": "Aegis Amulet Upgrade",
  "Item_Active_3": "",
  "Item_Active_4": "",
  "Item_Purch_1": "Bancroft's Talon",
  "Item_Purch_2": "Shoes of the Magi",
  "Item_Purch_3": "Evolved Shaman's Ring",
  "Item_Purch_4": "Spear of the Magus",
  "Item_Purch_5": "Chronos' Pendant",
  "Item_Purch_6": "Spear of Desolation",
  "Joust_Losses": 0,
  "Joust_Points": 0,
  "Joust_Tier": 0,
  "Joust_Wins": 0,
  "Killing_Spree": 6,
  "Kills_Bot": 69,
  "Kills_Double": 1,
  "Kills_Fire_Giant": 0,
  "Kills_First_Blood": 1,
  "Kills_Gold_Fury": 0,
  "Kills_Penta": 0,
  "Kills_Phoenix": 0,
  "Kills_Player": 14,
  "Kills_Quadra": 0,
  "Kills_Siege_Juggernaut": 0,
  "Kills_Single": 12,
  "Kills_Triple": 1,
  "Kills_Wild_Juggernaut": 0,
  "Map_Game": "Arena_V3",
  "Mastery_Level": 95,
  "Match": 943463607,
  "Match_Duration": 0,
  "MergedPlayers": null,
  "Minutes": 16,
  "Multi_kill_Max": 3,
  "Objective_Assists": 0,
  "PartyId": 0,
  "Rank_Stat_Conquest": 0,
  "Rank_Stat_Duel": 1506.25,
  "Rank_Stat_Joust": 1506.25,
  "Reference_Name": "Zeus",
  "Region": "NA",
  "Skin": "Uncle Zeus",
  "SkinId": 11567,
  "Structure_Damage": 0,
  "Surrendered": 0,
  "TaskForce": 2,
  "Team1Score": 0,
  "Team2Score": 34,
  "TeamId": 423171,
  "Team_Name": "ColombiaZ",
  "Time_In_Match_Seconds": 968,
  "Towers_Destroyed": 0,
  "Wards_Placed": 0,
  "Win_Status": "Winner",
  "Winning_TaskForce": 2,
  "hasReplay": "n",
  "hz_gamer_tag": null,
  "hz_player_name": "SrPoIo",
  "match_queue_id": 435,
  "name": "Normal: Arena",
  "playerId": "0",
  "playerName": "",
  "playerPortalId": null,
  "playerPortalUserId": null,
  "ret_msg": null
}
"""
