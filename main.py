import pandas as pd
from dota_preprocess_initial import *
from dota_ml import *




#training model on preprocessed data
#train_model(pd_data, 'radiant_win')


if __name__ == "__main__":
    running = True
    while running:
        mode = input("select mode:")
        if mode == "t":
            #reading json file containing Dota 2 matches into pandas DataFrame 
            pd_data = pd.read_json(open('dota_majors.json'))
            pd_data = preprocess(pd_data)
            train_model(pd_data, 'radiant_win')

        if mode == "p":
            data = input("enter game data:")
            data_array = data.split(",")
            df = pd.DataFrame([[data_array[i] for i in range(2)]], columns = TEAM_COLUMNS["rank"])
            df['picks_radiant'] = [sorted([data_array[i] for i in range(2,7)])]
            df['picks_dire'] = [sorted([data_array[i] for i in range(7,12)])]
            df = preprocess(df, pick_bans = False, id_to_rank = False)
            make_prediction(df)

        if mode == "k":
            train_model_split_keras(pd_data, 'radiant_win')

        if mode == "q":
            running = False


#train_model_split(pd_data, 'radiant_win')


    