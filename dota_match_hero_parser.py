import json
import os
from dota_ml import HEROES_JSON

MATCHES_JSON = json.load(open('parsed_matches.json'))




def create_winrates_empty(heroes):

    winrates_final = {}

    for hero in heroes:

        hero_id = hero["id"]
        winrates_inside = {}
        for hero_inside in heroes:
            hero_id_inside = hero_inside["id"]
            winrates_inside[hero_id_inside] = {"with" : {"wins" : 0, "total" : 0}, "against" : {"wins" : 0, "total" : 0}}
        winrates_final[hero_id] = winrates_inside
    
    return winrates_final


def get_parsed_winrates(matches, winrates):
    num = 0

    for match in matches:
        
        os.system('cls')
        print("{:.2f}".format(num/(len(matches) - 1)*100) + '%')
        num += 1

        for pick_first in match["picks_bans"]:

            if pick_first["is_pick"] == True:

                pick_first_hero_id = pick_first["hero_id"]

                for pick_second in match["picks_bans"]:

                    if pick_second["is_pick"] == True:

                        pick_second_hero_id = pick_second["hero_id"]

                        if pick_first["team"] == pick_second["team"]:

                            winrates[pick_first_hero_id][pick_second_hero_id]["with"]["total"] += 1

                            if pick_first["team"] == int(not match["radiant_win"]):

                                    winrates[pick_first_hero_id][pick_second_hero_id]["with"]["wins"] += 1
                        else:

                            winrates[pick_first_hero_id][pick_second_hero_id]["against"]["total"] += 1

                            if pick_first["team"] == int(not match["radiant_win"]):

                                winrates[pick_first_hero_id][pick_second_hero_id]["against"]["wins"] += 1
                        
                                      
winrates = create_winrates_empty(HEROES_JSON)
get_parsed_winrates(MATCHES_JSON, winrates)
file = open("winrates_final.json","w")
file.write(json.dumps(winrates, indent=2))