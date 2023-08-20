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

#adds teams relative winrate based on winrate of every hero of radiant team against every hero of dire team
def add_matchup_wr(row, heroes, matchups):
    team_wr_radiant = 0
    team_wr_dire = 0
    enemy_wr = 0
    division = 0

    #for every hero in radiant team adds its winrate percent against every hero in dire team
    for hero_name_radiant in row['picks_radiant']:
        num_wr_rad = 0
        num_wr_dir = 0
        divider = 1
        hero_id_radiant = next(hero['id'] for hero in heroes if hero["name"] == hero_name_radiant)
        hero_roles = next(hero['roles'] for hero in heroes if hero["id"] == hero_id_radiant)

        if 'Support' in hero_roles:
            divider += 0.1
        if 'Carry' in hero_roles:
            divider -= 0.1

        for hero_name_radiant_teammate in row["picks_radiant"]:
            hero_id_radiant_teammate = next(hero['id'] for hero in heroes if hero["name"] == hero_name_radiant_teammate)
            team_wr_radiant += matchups[str(hero_id_radiant)][str(hero_id_radiant_teammate)]["with"]
            num_wr_rad  += 1

        for hero_name_dire in row['picks_dire']:
            hero_id_dire = next(hero['id'] for hero in heroes if hero["name"] == hero_name_dire)
            enemy_wr += matchups[str(hero_id_radiant)][str(hero_id_dire)]["against"]
            division += divider

            for hero_name_dire_teammate in row["picks_dire"]:
                hero_id_dire_teammate = next(hero['id'] for hero in heroes if hero["name"] == hero_name_dire_teammate)
                team_wr_dire += matchups[str(hero_id_dire)][str(hero_id_dire_teammate)]["with"]
                num_wr_dir += 1
    #divides sum of winrates by their number, thus getting average winrate
    enemy_wr /= division
    team_wr_dire /= 125
    team_wr_radiant /= 25
    row['relative_winrate'] = enemy_wr
    row['dire_winrate'] = team_wr_dire
    row['radiant_winrate'] = team_wr_radiant

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

#splits a columns containing same size arrays into columns containing these arrays' elements
#df - DataFrame, col_name - name of a target column, num - length of arrays in this column
def split_array_col(df, col_name, num):
    df[[col_name + '_' + str(x + 1) for x in range(num)]] = pd.DataFrame(df[col_name].tolist(), index= df.index)
    return