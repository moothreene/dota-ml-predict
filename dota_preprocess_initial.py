import pandas as pd
from dota_ml import *
#reads a dictionary of picks/bans in pandas row and returns a row with str array, containing heroes names, according to their id
#row - row in Pandas DataFrame, heroes - dictionary with heroes names and ids


def preprocess(pd_data, winrate = True, pick_bans = True, id_to_rank = True):

    if pick_bans is True:
        #transforming picks_bans column from match data into an array of picked heroes names
        pd_data = pd_data.apply(dict_to_herolist, heroes = HEROES_JSON, axis = 'columns')
        pd_data = pd_data.drop(['picks_bans'],axis = 1)

    if winrate is True:
        #adding matchup relative winrate
        pd_data = pd_data.apply(add_matchup_wr, heroes = HEROES_JSON, matchups = MATCHUPS_JSON, axis = 'columns')
        
    if id_to_rank is True:
        #changing team IDs to team ranks
        pd_data = pd_data.apply(team_id_to_rank, teams = TEAMS_JSON, axis = 'columns')
        pd_data = pd_data.drop(['radiant_team_id','dire_team_id'], axis = 1)

    #splitting heroes names array into separate columns each containing one hero name    
    split_array_col(pd_data, 'picks_radiant', 5)
    split_array_col(pd_data, 'picks_dire', 5)
    pd_data = pd_data.drop(['picks_radiant','picks_dire', 'match_id' ], errors='ignore', axis = 1)

    return pd_data


def dict_to_herolist(row, heroes):

    picks_data = row['picks_bans']
    team_radiant = []
    team_dire = []

    if row['picks_bans'] is not None:
        for pick_ban in picks_data:

            #selecting only picked heroes
            if pick_ban['is_pick'] == True:
                hero = next(hero["name"] for hero in heroes if hero["id"] == pick_ban['hero_id'])

                #dividing picked heroes by their respective team, 0 being radiant and 1 dire
                if pick_ban['team'] == 0:
                    team_radiant.append(hero)
                else:
                    team_dire.append(hero)


    #adding arrays with hero names to DataFrame row
    row['picks_radiant'] = sorted(team_radiant)
    row['picks_dire'] = sorted(team_dire)
    return row

#adds teams relative winrate based on winrate of every hero of radiant team against every hero of dire team
#row - row in Pandas DataFrame, heroes - json with heroes names and ids, matchups - json with hero matchups: wins and total games played
def add_matchup_wr(row, heroes, matchups):

    #initializing winrate variables
    team_wr_radiant = 0
    team_wr_dire = 0
    relative_wr = 0
    division = 0

    #cycling through radiant team heroes
    for hero_name_radiant in row['picks_radiant']:

        #initializing divider for weighted winrate
        divider = 1
        #getting hero id and roles
        hero_id_radiant = next(hero['id'] for hero in heroes if hero["name"] == hero_name_radiant)
        hero_roles = next(hero['roles'] for hero in heroes if hero["id"] == hero_id_radiant)

        #if a hero is support, his winrate weights less and otherwise
        if 'Support' in hero_roles:
            divider += 0.1
        if 'Carry' in hero_roles:
            divider -= 0.1

        #cycling through radiant team once again to get winrates of radiant heroes with their teammates
        for hero_name_radiant_teammate in row["picks_radiant"]:
            hero_id_radiant_teammate = next(hero['id'] for hero in heroes if hero["name"] == hero_name_radiant_teammate)
            team_wr_radiant += matchups[str(hero_id_radiant)][str(hero_id_radiant_teammate)]["with"]

        #cycling through dire team to get winrates of radiant heroes against them
        for hero_name_dire in row['picks_dire']:
            hero_id_dire = next(hero['id'] for hero in heroes if hero["name"] == hero_name_dire)
            relative_wr += matchups[str(hero_id_radiant)][str(hero_id_dire)]["against"]
            division += divider

            #cycling through dire team once again to get winrates of dire heroes with their teammates
            for hero_name_dire_teammate in row["picks_dire"]:
                hero_id_dire_teammate = next(hero['id'] for hero in heroes if hero["name"] == hero_name_dire_teammate)
                team_wr_dire += matchups[str(hero_id_dire)][str(hero_id_dire_teammate)]["with"]

    #divides sum of winrates by divider, thus getting weighted average winrate
    relative_wr /= division

    #dividing winrate sum of radiant and dire team by a number of winrates to get average winrate
    team_wr_dire /= 125
    team_wr_radiant /= 25

    #adding new values to DataFrame row
    row['relative_winrate'] = relative_wr
    row['dire_winrate'] = team_wr_dire
    row['radiant_winrate'] = team_wr_radiant

    return row

#gets team id in pandas row and returns a row with a team rank according to it's id
#row - row in Pandas DataFrame, teams - dictionary with team names, ids and ranks
def team_id_to_rank(row, teams):

    radiant_team_id = row["radiant_team_id"]
    dire_team_id = row["dire_team_id"]
    team_radiant = next(team["rank"] for team in teams if team["id"] == radiant_team_id)
    team_dire = next(team["rank"] for team in teams if team["id"] == dire_team_id)

    #adding team ranks to DataFrame row
    row['radiant_team_rank'] = int(team_radiant)
    row['dire_team_rank'] = int(team_dire)

    return row

#gets team id in pandas row and returns a row with a team name according to it's id
#row - row in Pandas DataFrame, teams - dictionary with team names and ids
def team_id_to_name(row, teams):

    radiant_team_id = row["radiant_team_id"]
    dire_team_id = row["dire_team_id"]
    team_radiant = next(team["name"] for team in teams if team["id"] == radiant_team_id)
    team_dire = next(team["name"] for team in teams if team["id"] == dire_team_id)

    #adding team names to DataFrame row
    row['radiant_team_name'] = team_radiant
    row['dire_team_name'] = team_dire

    return row

def team_name_to_id(row, teams):

    radiant_team_name = row["radiant_team_name"]
    dire_team_name = row["dire_team_name"]
    team_radiant = next(team["id"] for team in teams if team["name"] == radiant_team_name)
    team_dire = next(team["id"] for team in teams if team["name"] == dire_team_name)

    #adding team names to DataFrame row
    row['radiant_team_id'] = team_radiant
    row['dire_team_id'] = team_dire

    return row

#splits a columns containing same size arrays into columns containing these arrays' elements
#df - DataFrame, col_name - name of a target column, num - length of arrays in this column
def split_array_col(df, col_name, num):
    df[[col_name + '_' + str(x + 1) for x in range(num)]] = pd.DataFrame(df[col_name].tolist(), index= df.index)
    return