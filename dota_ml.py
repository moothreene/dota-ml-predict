from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import layers


#reading hero names from heroes list and adding them into array to use as OH encoder categories
HEROES = []
HEROES_NAMES = []

#reading json file containing Dota 2 heroes into dictionary
HEROES_JSON = json.load(open('dota_heroes.json'))
for hero in HEROES_JSON:
    HEROES.append(hero['name'])
    HEROES_NAMES.append(hero['localized_name'])


#reading team names from teams list and adding them into array to use as OH encoder categories    
TEAMS = []


#reading json file containing Dota 2 teams into dictionary
TEAMS_JSON = json.load(open('dota_teams.json'))
for team in TEAMS_JSON:
    TEAMS.append(team['name'])


#columns for picks splitting
HERO_COLUMNS = ['picks_radiant_1', 'picks_radiant_2', 'picks_radiant_3','picks_radiant_4','picks_radiant_5',
                 'picks_dire_1', 'picks_dire_2', 'picks_dire_3', 'picks_dire_4', 'picks_dire_5']


#columns for team names
TEAM_COLUMNS = {
    "name": ['team_radiant', 'team_dire'],
    "rank": ['radiant_team_rank', 'dire_team_rank']
}


TEAM_RANK_COLUMNS = []

#reading json file containing Dota 2 hero matchups into dictionary
MATCHUPS_JSON = json.load(open('dota_winrates_by_hero.json'))


#OH encodes data that was split for evaluation purposes and returns encoded data
#X_train, X_valid - results of train_test_split method
def OH_encode_train(X_train, X_valid, target_columns, categories):

    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(categories = [categories for i in target_columns], handle_unknown = 'ignore', sparse = False)

    #OH encoding object columns
    OH_X_train_col = pd.DataFrame(OH_encoder.fit_transform(X_train[target_columns]), columns = OH_encoder.get_feature_names_out(target_columns))
    OH_X_valid_col = pd.DataFrame(OH_encoder.transform(X_valid[target_columns]), columns = OH_encoder.get_feature_names_out(target_columns))

    #bringing back an index, dropped by OH encoding and making sure that encoded columns are of str type
    OH_X_train_col.index = X_train.index
    OH_X_valid_col.index = X_valid.index
    OH_X_train_col.columns = OH_X_train_col.columns.astype(str)
    OH_X_valid_col.columns = OH_X_valid_col.columns.astype(str)

    #getting number columns from original DataFrame and adding them to encoded object columns
    return OH_X_train_col, OH_X_valid_col
    

#OH encodes data and returns encoded data
#X - data for encoding
def OH_encode(X, target_columns, categories):

    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(categories = [categories for i in target_columns], handle_unknown = 'ignore', sparse = False)
    #OH encoding object columns    
    OH_X_col = pd.DataFrame(OH_encoder.fit_transform(X[target_columns]), columns = OH_encoder.get_feature_names_out(target_columns))
    #bringing back an index, dropped by OH encoding and making sure that encoded columns are of str type
    OH_X_col.index = X.index
    OH_X_col.columns = OH_X_col.columns.astype(str)

    return OH_X_col


def preprocess_final(X):

    #OneHotEncoding X
    OH_X_HEROES = OH_encode(X, HERO_COLUMNS, HEROES)

    #getting number columns from original DataFrame and adding them to encoded object columns
    num_X_col = X.drop(HERO_COLUMNS, axis = 1)
    OH_X_full = pd.concat([num_X_col, OH_X_HEROES], axis = 1)

    OH_X_full.columns = OH_X_full.columns.astype(str)

    return OH_X_full

def preprocess_final_split(X_train, X_valid):

    #OneHotEncoding X
    OH_X_HEROES_train, OH_X_HEROES_valid = OH_encode_train(X_train, X_valid, HERO_COLUMNS, HEROES)

    #getting number columns from original DataFrame and adding them to encoded object columns
    num_X_col_train = X_train.drop(HERO_COLUMNS, axis = 1)
    num_X_col_valid = X_valid.drop(HERO_COLUMNS, axis = 1)

    OH_X_train_full = pd.concat([num_X_col_train, OH_X_HEROES_train], axis = 1)
    OH_X_valid_full = pd.concat([num_X_col_valid, OH_X_HEROES_valid], axis = 1)

    OH_X_train_full.columns = OH_X_train_full.columns.astype(str)
    OH_X_valid_full.columns = OH_X_valid_full.columns.astype(str)

    return OH_X_train_full, OH_X_valid_full
    

#sets up and trains machine learning model on given data, saving model as "finalized_model.sav"
#data - data to train on, col - target column
def train_model(data, target_col):
    #dividing DataFrame into y - target column and X - the rest
    X = data.drop([target_col], axis = 1)
    y = data[target_col] 

    #setting up ml model
    model = RandomForestRegressor(random_state=0)

    #OH encoding heroes and teams
    X_final = preprocess_final(X)
    X_final = X_final.reindex(sorted(X_final.columns), axis=1)
    #fitting data into model
    model.fit(X_final, y)

    #saving model to disk for later use
    pickle.dump(model, open('finalized_model.sav', 'wb'))
    print("complete!")


def train_model_split(data, target_col):
    
    #dividing DataFrame into y - target column and X - the rest
    X = data.drop([target_col], axis = 1)
    y = data[target_col] 
    X_train, X_valid, y_train, y_valid = train_test_split(X, y,test_size = 0.2)

    #setting up ml model
    model_forest = RandomForestRegressor(random_state = 0)

    #OH encoding heroes and teams
    X_train_final, X_valid_final = preprocess_final_split(X_train, X_valid)
    #fitting data into model
    model_forest.fit(X_train_final, y_train)
    preds_forest = model_forest.predict(X_valid_final)
    print(mean_absolute_error(y_valid, preds_forest))



def train_model_split_keras(data, target_col):
    
    #dividing DataFrame into y - target column and X - the rest
    X = data.drop([target_col], axis = 1)
    y = data[target_col] 
    X_train, X_valid, y_train, y_valid = train_test_split(X, y,test_size = 0.2)

    #setting up ml model

    #OH encoding heroes and teams
    X_train_final, X_valid_final = preprocess_final_split(X_train, X_valid)

    model_keras = keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=[1245]),
        layers.Dense(256, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(1)
    ])
    model_keras.compile(
        optimizer="adam",
        loss="mae"
    )
    history = model_keras.fit(
        X_train_final, y_train,
        validation_data=(X_valid_final, y_valid),
        batch_size=256,
        epochs=250
    )
    history_df = pd.DataFrame(history.history)
# use Pandas native plot method
    #fitting data into model




def make_prediction(data):
    data = preprocess_final(data)
    data = data.reindex(sorted(data.columns), axis=1)
    model = pickle.load(open('finalized_model.sav', 'rb'))
    print(model.predict(data))