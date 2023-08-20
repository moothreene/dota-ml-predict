import requests
import json
import time
import os


def get_matchups_wr(id, matchups):
    matchups_wr = {'id' : id}
    for matchup in matchups:
        wr = matchup['wins'] / matchup['games_played']
        matchups_wr[matchup['hero_id']] = wr

    return matchups_wr


def matchups():
    json_out = []

    for hero_id in range(1,139):
        os.system('cls')
        print("{:.2f}".format(hero_id/1.38)+"%")
        url = "https://api.opendota.com/api/heroes/" + str(hero_id) + "/matchups"
        response = requests.get(url)
        if response.status_code == 200 and response.json() != []:
            json_out.append(get_matchups_wr(hero_id, response.json()))
            time.sleep(2)
    file = open("matchup_winrates.json","w")
    file.write(json.dumps(json_out, indent=2))


def pro_matches():
    url = 'https://api.opendota.com/api/parsedMatches'
    response = requests.get(url, params = {"less_than_match_id": 7284600275})
    out = response.json()
    print(out)

    
def hero_matches():

    url = 'https://api.opendota.com/api/heroes/2/matches'
    response = requests.get(url, params = {"less_than_match_id": 7284600275})
    out = response.json()
    print(out)


def find_matches(teamA, teamB):

    params = {"teamA":teamA, "teamB":teamB, "limit": 1000}
    url = 'https://api.opendota.com/api/findMatches'
    response = requests.get(url, params = params)
    out = response.json()
    wins = 0
    for match in out:
        if match['teamawin'] == True:
            wins += 1


def heroes():
    url = 'https://api.opendota.com/api/heroes'
    response = requests.get(url)
    out = response.json()
    file = open("heroes_from_api.json","w")
    file.write(json.dumps(out, indent=2))


def explorer():
    query_league = """
                    SELECT
                    match_id,
                    radiant_win,
                    radiant_team_id,
                    dire_team_id,
                    picks_bans
                    FROM matches
                    JOIN leagues using(leagueid)
                    WHERE TRUE
                    AND matches.leagueid = 15475
                    AND matches.start_time >= extract(epoch from timestamp '2023-07-05T16:00:51.067Z')
                    GROUP BY matches.match_id
                    HAVING count(distinct match_id) >= 1
                    ORDER BY matches.match_id
                """
    query_2022 = """
                    SELECT
                    match_id,
                    radiant_win,
                    picks_bans
                    FROM matches
                    WHERE TRUE
                    AND matches.start_time >= extract(epoch from timestamp '2022-01-01T00:00:00.000Z')
                    AND NOT picks_bans IS NULL
                    GROUP BY matches.match_id
                    HAVING count(distinct match_id) >= 1
                    ORDER BY matches.match_id
                """

    params_league = {"sql" : query_league}
    params_reg = {"sql" : query_2022}
    url = 'https://api.opendota.com/api/explorer'
    response = requests.get(url, params = params_reg)
    out = response.json()
    print(out["rowCount"])
    file = open("parsed_matches.json","w")
    file.write(json.dumps(out["rows"], indent=2))


explorer()