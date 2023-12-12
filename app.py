from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from dota_preprocess_initial import *
from dota_ml import *
import os

app=Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Home"

@app.route("/get-pred/<data>")
def get_pred(data):
    data_array = data.split(",")
    df = pd.DataFrame([[data_array[i] for i in range(2)]], columns = TEAM_COLUMNS["rank"])
    df['picks_radiant'] = [sorted([data_array[i] for i in range(2,7)])]
    df['picks_dire'] = [sorted([data_array[i] for i in range(7,12)])]
    df = preprocess(df, pick_bans = False, id_to_rank = False)
    try:
        pred = make_prediction(df)
    except:
        return jsonify("Error!"), 404
    return jsonify(pred), 200

if(__name__) == "__main__":
    app.debug = False
    from waitress import serve
    port = int(os.environ.get('PORT', 33507))
    serve(app, port=port)