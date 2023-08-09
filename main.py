import pandas as pd
import json
from dota_parse_picks import *
from dota_ml import *
if __name__ == "__main__":

    json_data = open('dota_majors.json')
    json_heroes = open('heroes.json')
    test_heroes = json.load(json_heroes)
    pd_data = pd.read_json(json_data)

    pd_data = pd_data.apply(dict_to_teamlist, heroes = test_heroes, axis = 'columns')

    pd_data = pd_data.drop(['picks_bans'],axis = 1)

    split_array_col(pd_data, 'picks_radiant', 5)
    split_array_col(pd_data, 'picks_dire', 5)

    pd_data = pd_data.drop(['picks_radiant','picks_dire'], axis = 1)
    train_model(pd_data, 'radiant_win')


    