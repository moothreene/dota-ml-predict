#from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import openpyxl

def train_model(data, col):
    y = data[col]
    ids = data['match_id']
    X = data.drop([col,'match_id'], axis = 1)
    object_columns = (X.dtypes == 'object')
    object_columns = list(object_columns[object_columns].index)
    OH_encoder = OneHotEncoder(handle_unknown = 'ignore', sparse = False)
    #train_X, val_X, train_y, val_y = train_test_split(X, y, random_state= 0)

    #OH_train_X_col = pd.DataFrame(OH_encoder.fit_transform(train_X[object_columns]))
    #OH_val_X_col = pd.DataFrame(OH_encoder.transform(val_X[object_columns]))
    OH_X_col = pd.DataFrame(OH_encoder.fit_transform(X[object_columns]))

    #OH_train_X_col.index = train_X.index
    #OH_val_X_col.index = val_X.index
    OH_X_col.index = X.index

    #num_train_X = train_X.drop(object_columns, axis = 1)
    #num_val_X = val_X.drop(object_columns, axis = 1)
    num_X = X.drop(object_columns, axis = 1)

    #OH_train_X = pd.concat([num_train_X, OH_train_X_col], axis = 1)
    #OH_val_X = pd.concat([num_val_X, OH_val_X_col], axis = 1)
    OH_X = pd.concat([num_X, OH_X_col], axis = 1)

    #OH_train_X.columns = OH_train_X.columns.astype(str)
    #OH_val_X.columns = OH_val_X.columns.astype(str)
    OH_X.columns = OH_X.columns.astype(str)

    model = RandomForestRegressor(n_estimators=200, min_samples_split=20, random_state=0)

    #print(score_model(model,OH_train_X, OH_val_X, train_y, val_y))

    model.fit(OH_X, y)
    preds = model.predict(OH_X)
    out = pd.concat([ids, pd.DataFrame(preds, columns = ['Prediction']), y ], axis = 1)
    out.to_excel('Preds.xlsx')

def score_model(model, X_t, X_v, y_t, y_v):
    model.fit(X_t, y_t)
    preds = model.predict(X_v)
    return mean_absolute_error(y_v, preds)