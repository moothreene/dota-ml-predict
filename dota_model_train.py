import pandas as pd
from dota_preprocess_initial import *
from dota_ml import *

#reading json file containing Dota 2 matches into pandas DataFrame 
pd_data = pd.read_json(open('dota_majors.json'))

#transforming picks_bans column from match data into an array of picked heroes names
pd_data = pd_data.apply(dict_to_herolist, heroes = HEROES_JSON, axis = 'columns')
pd_data = pd_data.drop(['picks_bans'],axis = 1)

#adding matchup relative winrate
pd_data = pd_data.apply(add_matchup_wr, heroes = HEROES_JSON, matchups = MATCHUPS_JSON, axis = 'columns')

#splitting heroes names array into separate columns each containing one hero name
split_array_col(pd_data, 'picks_radiant', 5)
split_array_col(pd_data, 'picks_dire', 5)
pd_data = pd_data.drop(['picks_radiant','picks_dire'], axis = 1)

#changing team IDs to team names
pd_data = pd_data.apply(team_id_to_rank, teams = TEAMS_JSON, axis = 'columns')
pd_data = pd_data.drop(['radiant_team_id','dire_team_id','match_id'], axis = 1)

print(pd_data.head())
#training model on preprocessed data
#train_model(pd_data, 'radiant_win')

train_model_split(pd_data, 'radiant_win')


    