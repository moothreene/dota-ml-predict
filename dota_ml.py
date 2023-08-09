from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

import openpyxl
from sklearn.model_selection import train_test_split

#OH encodes data that was split for evaluation purposes and returns encoded data
#X_train, X_valid - results of train_test_split method
def OH_encode_train(X_train, X_valid):

    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(handle_unknown = 'ignore', sparse = False)
    object_columns = (X_train.dtypes == 'object')
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
    #setting up the encoder and getting a list of object columnd
    OH_encoder = OneHotEncoder(handle_unknown = 'ignore', sparse = False)
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

#sets up and trains machine learning model on given data, saving results as excel file
#data - data to train on, col - target column
def train_model(data, col):

    #dividing DataFrame into y - target column and X - the rest
    X = data.drop([col,'match_id'], axis = 1)
    y = data[col]
    
    #X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state= 0)  - for mae validation

    #OneHotEncoding X
    OH_X = OH_encode(X)
    #OH_X_train, OH_X_valid = OH_encode_train(X_train, X_valid) - for mae validation

    #setting up ml model
    model = RandomForestRegressor(n_estimators=200, min_samples_split=20, random_state=0)

    #print(score_model(model,OH_X_train, OH_X_valid, y_train, y_valid)) - for mae validation

    #fitting data into model
    model.fit(OH_X, y)

    #making predictions and saving them as excel file
    preds = model.predict(OH_X)
    out = pd.concat([data['match_id'], pd.DataFrame(preds, columns = ['Prediction']), y ], axis = 1)
    out.to_excel('Preds.xlsx')

#returns mae score for a model
#model - model to score, X_t, X_v, y_t, y_v - results of train_test_split method
def score_model(model, X_t, X_v, y_t, y_v):
    model.fit(X_t, y_t)
    preds = model.predict(X_v)
    return mean_absolute_error(y_v, preds)