from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split

#OH encodes data that was split for evaluation purposes and returns encoded data
#X_train, X_valid - results of train_test_split method
def OH_encode_train(X_train, X_valid):

    #reading hero names from heroes list and adding them into array to use as OH encoder categories
    HEROES = []
    json_heroes = open('dota_heroes.json')
    test_heroes = json.load(json_heroes)
    for hero in test_heroes:
        HEROES.append(hero['name'])

    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(categories = [HEROES for i in range(10)], handle_unknown = 'ignore', sparse = False)
    object_columns = (pd.concat([X_train, X_valid]).dtypes == 'object')
    object_columns = list(object_columns[object_columns].index)

    #OH encoding object columns
    OH_X_train_col = pd.DataFrame(OH_encoder.fit_transform(X_train[object_columns]))
    OH_X_valid_col = pd.DataFrame(OH_encoder.transform(X_valid[object_columns]))

    #bringing back an index, dropped by OH encoding and making sure that encoded columns are of str type
    OH_X_train_col.index = X_train.index
    OH_X_valid_col.index = X_valid.index
    OH_X_train_col.columns = OH_X_train_col.columns.astype(str)
    OH_X_valid_col.columns = OH_X_valid_col.columns.astype(str)

    #getting number columns from original DataFrame and adding them to encoded object columns
    num_X_train_col = X_train.drop(object_columns, axis = 1)
    num_X_valid_col = X_valid.drop(object_columns, axis = 1)
    X_train_full = pd.concat([num_X_train_col, OH_X_train_col], axis = 1)
    X_valid_full = pd.concat([num_X_valid_col, OH_X_valid_col], axis = 1)

    return X_train_full, X_valid_full
    
#OH encodes data and returns encoded data
#X - data for encoding
def OH_encode(X):

    #reading hero names from heroes list and adding them into array to use as OH encoder categories
    HEROES = []
    json_heroes = open('dota_heroes.json')
    test_heroes = json.load(json_heroes)
    for hero in test_heroes:
        HEROES.append(hero['name'])

    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(categories = [HEROES for i in range(10)], handle_unknown = 'ignore', sparse = False)
    object_columns = (X.dtypes == 'object')
    object_columns = list(object_columns[object_columns].index)

    #OH encoding object columns    
    OH_X_col = pd.DataFrame(OH_encoder.fit_transform(X[object_columns]))

    #bringing back an index, dropped by OH encoding and making sure that encoded columns are of str type
    OH_X_col.index = X.index
    OH_X_col.columns = OH_X_col.columns.astype(str)

    #getting number columns from original DataFrame and adding them to encoded object columns
    num_X_col = X.drop(object_columns, axis = 1)
    X_full = pd.concat([num_X_col, OH_X_col], axis = 1)

    return X_full

#sets up and trains machine learning model on given data, saving model as "finalized_model.sav"
#data - data to train on, col - target column
def train_model(data, col):
    #dividing DataFrame into y - target column and X - the rest
    X = data.drop([col,'match_id'], axis = 1)
    y = data[col]
    #X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state= 0)# - MAE check

    #OneHotEncoding X
    OH_X = OH_encode(X)
    #OH_X_train, OH_X_valid = OH_encode_train(X_train, X_valid)# - MAE check

    #setting up ml model
    model = RandomForestRegressor(random_state=0)

    #fitting data into model
    model.fit(OH_X, y)
    #model.fit(OH_X_train, y_train)# - MAE check
    
    #saving model to disk for later use
    pickle.dump(model, open('finalized_model.sav', 'wb'))

#returns mae score for a model
#model - model to score, X_t, X_v, y_t, y_v - results of train_test_split method
def score_model(model, X_t, X_v, y_t, y_v):
    model.fit(X_t, y_t)
    preds = model.predict(X_v)
    return mean_absolute_error(y_v, preds)