import pandas as pd
import json
from dota_parse_picks import *
from dota_ml import *

if __name__ == "__main__":

    #reading json file containing Dota 2 matches into pandas DataFrame
    json_data = open('dota_majors.json')
    pd_data = pd.read_json(json_data)

    #reading json file containing Dota 2 heroes into dictionary
    json_heroes = open('dota_heroes.json')
    test_heroes = json.load(json_heroes)
    
    #transforming picks_bans column from match data into an array of picked heroes names
    pd_data = pd_data.apply(dict_to_herolist, heroes = test_heroes, axis = 'columns')
    pd_data = pd_data.drop(['picks_bans'],axis = 1)

    #splitting heroes names array into separate columns each containing one hero name
    split_array_col(pd_data, 'picks_radiant', 5)
    split_array_col(pd_data, 'picks_dire', 5)
    pd_data = pd_data.drop(['picks_radiant','picks_dire'], axis = 1)

    #training model on preprocessed data
    train_model(pd_data, 'radiant_win')


    