#the list of match ids
ids_list = [944268806,944268805,944268804,944268803,944268802,944268801,944268800,944268799,944268797,944268796,944268795,944268794,944268793,944268792,944268791,944268790,944268789,944268788,944268787,944268786,944268785,944268783,944268782,944268781,944268780,944268779,944268778,944268777,944268776,944268775,944268774,944268773,944268771,944268770,944268769,944268768,944268767,944268766,944268765,944268763,944268761,944268760,944268759,944268758,944268757,944268756,944268755,944268754,944268753,944268342,944268341,944268340,944268339,944268338,944268337,944268336,944268335,944268334,944268333,944268331,944268330,944268329,944268328,944268327,944268326,944268325,944268324,944268323,944268322,944268321,944268320,944268319,944268318,944268317,944268316,944268315,944268314,944268313,944268312,944268311,944268310,944268284,944268283,944268282,944268281,944268280,944268279,944268278,944268277,944268276,944268275,944268274,944268272,944268271,944267926,944267925,944267924,944267923,944267922,944267921,944267919,944267918,944267917,944267916,944267915,944267914,944267913,944267912,944267911,944267910,944267909,944267908,944267907,944267906,944267905,944267904,944267903,944267902,944267901,944267900,944267899,944267898,944267896,944267895,944267894,944267893,944267892,944267891,944267890,944267889,944267888,944267887,944267886,944267885,944267883,944267882,944267881,944267880,944267879,944267878,944267877,944267876,944267875,944267873,944267872,944267871,944267870,944267869,944267868,944267867,944267422,944267421,944267420,944267419,944267418,944267417,944267416,944267415,944267414,944267413,944267412,944267411]

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
