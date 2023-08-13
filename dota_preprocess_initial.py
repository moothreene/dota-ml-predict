import pandas as pd

#reads a dictionary of picks/bans in pandas row and returns a row with str array, containing heroes names, according to their id
#row - row in Pandas DataFrame, heroes - dictionary with heroes names and ids
def dict_to_herolist(row, heroes):

    picks_data = row['picks_bans']
    team_radiant = []
    team_dire = []

    if row['picks_bans'] != None:
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

#gets team id in pandas row and returns a row with a team name according to it's id
#row - row in Pandas DataFrame, teams - dictionary with team names and ids
def team_id_to_name(row, teams):
    radiant_team_id = row["radiant_team_id"]
    dire_team_id = row["dire_team_id"]
    team_radiant = next(team["name"] for team in teams if team["id"] == radiant_team_id)
    team_dire = next(team["name"] for team in teams if team["id"] == dire_team_id)

    #adding team names to DataFrame row
    row['team_radiant'] = team_radiant
    row['team_dire'] = team_dire
    return row


def team_name_to_id(row, teams):
    radiant_team_name= row["team_radiant"]
    dire_team_name = row["team_dire"]
    team_radiant_id = next(team["id"] for team in teams if team["name"] == radiant_team_name)
    team_dire_id = next(team["id"] for team in teams if team["name"] == dire_team_name)

    row['radiant_team_id'] = team_radiant_id
    row['dire_team_id'] = team_dire_id
    return row

#splits a columns containing same size arrays into columns containing these arrays' elements
#df - DataFrame, col_name - name of a target column, num - length of arrays in this column
def split_array_col(df, col_name, num):
    df[[col_name + '_' + str(x + 1) for x in range(num)]] = pd.DataFrame(df[col_name].tolist(), index= df.index)
    return