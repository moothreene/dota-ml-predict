import pandas as pd

def dict_to_teamlist(row, heroes):
    picks_data = row['picks_bans']
    team_radiant = []
    team_dire = []

    if row['picks_bans'] != None:
        for pick_ban in picks_data:
            if pick_ban['is_pick'] == True:
                hero = next(hero["name"] for hero in heroes if hero["id"] == pick_ban['hero_id'])
                if pick_ban['team'] == 0:
                    team_radiant.append(hero)
                else:
                    team_dire.append(hero)

    row['picks_radiant'] = team_radiant
    row['picks_dire'] = team_dire
    return row 

def split_array_col(df, col_name, num):
    df[[col_name + '_' + str(x + 1) for x in range(num)]] = pd.DataFrame(df[col_name].tolist(), index= df.index)
    return