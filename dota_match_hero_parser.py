import json
import os
import pandas as pd
from dota_ml import HEROES_JSON

MATCHES_JSON = json.load(open('parsed_matches.json'))




def create_matchups_empty(heroes):

    matchups_final = {}

    for hero in heroes:

        hero_id = hero["id"]
        matchups_internal = {}
        for hero_inside in heroes:
            hero_id_inside = hero_inside["id"]
            matchups_internal[hero_id_inside] = {"with" : {"wins" : 0, "total" : 0}, "against" : {"wins" : 0, "total" : 0}}
        matchups_final[hero_id] = matchups_internal
    
    return matchups_final


def get_parsed_matchups(matches, matchups):
    num = 0

    for match in matches:
        
        os.system('cls')
        print("{:.2f}".format(num/(len(matches) - 1)*100) + '%')
        num += 1

        for pick_first in match["picks_bans"]:

            if pick_first["is_pick"] is True:

                pick_first_hero_id = pick_first["hero_id"]

                for pick_second in match["picks_bans"]:

                    if pick_second["is_pick"] is True:

                        pick_second_hero_id = pick_second["hero_id"]

                        if pick_first["team"] == pick_second["team"]:

                            matchups[pick_first_hero_id][pick_second_hero_id]["with"]["total"] += 1

                            if pick_first["team"] == int(not match["radiant_win"]):

                                    matchups[pick_first_hero_id][pick_second_hero_id]["with"]["wins"] += 1
                        else:

                            matchups[pick_first_hero_id][pick_second_hero_id]["against"]["total"] += 1

                            if pick_first["team"] == int(not match["radiant_win"]):

                                matchups[pick_first_hero_id][pick_second_hero_id]["against"]["wins"] += 1
                        


def hero_matchups_to_winrates(matchups):

    CONST_WINRATE = 5

    winrates_percentage = {}

    for hero_id in matchups:

        winrates_per_hero = {}

        for hero_id_internal in matchups[hero_id]:

            stats = matchups[hero_id][hero_id_internal]

            if stats["with"]["total"] != 0:

                winrate_with = (stats["with"]["wins"] + 5) / (stats["with"]["total"] + 10)
            else:

                winrate_with = 0.5

            if stats["against"]["total"] != 0:

                winrate_against = (stats["against"]["wins"] + 5) / (stats["against"]["total"] + 10)
            else:
                winrate_against = 0.5

            winrates_per_hero[hero_id_internal] = {"with" : winrate_with, "against" : winrate_against}

        winrates_percentage[hero_id] = winrates_per_hero

    return winrates_percentage


'''matchups = create_matchups_empty(HEROES_JSON)
get_parsed_matchups(MATCHES_JSON, matchups)
file = open("dota_hero_matchups.json","w")
file.write(json.dumps(matchups, indent = 2))'''

WINRATES_JSON = json.load(open('dota_hero_matchups.json'))

winrates = hero_matchups_to_winrates(WINRATES_JSON)
file = open("dota_winrates_by_hero.json", "w")
file.write(json.dumps(winrates, indent = 2))


'''heroes_with = []

for hero_id in winrates:
    hero_array = []
    for hero_id_internal in winrates[hero_id]:
        hero_array.append(winrates[hero_id][hero_id_internal]["with"])
    heroes_with.append(hero_array)

df = pd.DataFrame(heroes_with)
df.columns = [hero["id"] for hero in HEROES_JSON]
df.to_excel("winrates.xlsx")'''