import pickle
import pandas as pd
import json
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteEntry
from dota_ml import preprocess_final, TEAM_COLUMNS, HERO_COLUMNS, HEROES, TEAMS, MATCHUPS_JSON, HEROES_JSON, HEROES_NAMES
from dota_preprocess_initial import add_matchup_wr


#creates pd dataframe from entry values and predicts value based on it
def read_text():

    #getting entry data from teams and picks entry widgets and combining them into a single array
    team_data = [input_radiant_teamid.get(), input_dire_teamid.get()]
    picks_data = [(entry.get()) for entry in (radiant_inputs + dire_inputs)]
    data = team_data + picks_data
    #creating pandas DataFrame with 1 row, based on entry values
    df = pd.DataFrame([data], columns = TEAM_COLUMNS + HERO_COLUMNS)

    df = df.apply(add_picks_array, picks = picks_data, axis = 'columns')
    df = df.apply(add_matchup_wr, heroes = HEROES_JSON, matchups = MATCHUPS_JSON, axis = 'columns')
    df = df.drop(['picks_radiant','picks_dire'], axis = 1)
    #making a prediction from entry data
    prediction = ml_predict(df)

    #changing label text to show prediction value
    label_prediction.config(text = prediction)


def add_picks_array(row, picks):

    row['picks_radiant'] = picks[:5]
    row['picks_dire'] = picks[5:]

    return row


#predicts outcome based on data by loading ml model
def ml_predict(data):
    #loading ml model   
    model = pickle.load(open('finalized_model.sav', 'rb'))
    data = preprocess_final(data)
    return model.predict(data)


if __name__ == "__main__":

    #creating tkinter screen entity
    root = Tk()
    root.geometry('400x500')
    root.title('Dota match predictions')

    #creating LabelFrame for Radiant team
    radiant_lf = LabelFrame(root, text = 'Radiant')

    #creating team id Label and Entry and putting them into LabelFrame grid
    Label(radiant_lf, text = 'Radiant team:').grid(row = 0, column = 0, sticky = W)
    input_radiant_teamid = AutocompleteEntry(radiant_lf, completevalues = TEAMS)
    input_radiant_teamid.grid(row = 0, column = 1)

    #creating pick entries and adding them into an array
    input_radiant_1 = AutocompleteEntry(radiant_lf, completevalues = HEROES)
    input_radiant_2 = AutocompleteEntry(radiant_lf, completevalues = HEROES)
    input_radiant_3 = AutocompleteEntry(radiant_lf, completevalues = HEROES)
    input_radiant_4 = AutocompleteEntry(radiant_lf, completevalues = HEROES)
    input_radiant_5 = AutocompleteEntry(radiant_lf, completevalues = HEROES)

    radiant_inputs = [input_radiant_1, input_radiant_2, input_radiant_3, input_radiant_4, input_radiant_5]

    #creating Label for each pick entry and putting them into LabelFrame grid
    for i in range(5):
        Label(radiant_lf, text = ('Radiant hero ' + str(i + 1) + ':')).grid(row = i+1, column = 0, sticky = W)
        radiant_inputs[i].grid(row = i + 1, column = 1)

    #creating LabelFrame for Dire team
    dire_lf = LabelFrame(root, text = 'Dire')

    #creating team id Label and Entry and putting them into LabelFrame grid
    Label(dire_lf, text = 'Dire team:').grid(row = 0, column = 0, sticky = W)
    input_dire_teamid = AutocompleteEntry(dire_lf, completevalues = TEAMS)
    input_dire_teamid.grid(row = 0, column = 1, padx = (20,0))

    #creating pick entries and adding them into an array
    input_dire_1 = AutocompleteEntry(dire_lf, completevalues = HEROES)
    input_dire_2 = AutocompleteEntry(dire_lf, completevalues = HEROES)
    input_dire_3 = AutocompleteEntry(dire_lf, completevalues = HEROES)
    input_dire_4 = AutocompleteEntry(dire_lf, completevalues = HEROES)
    input_dire_5 = AutocompleteEntry(dire_lf, completevalues = HEROES)

    dire_inputs = [input_dire_1, input_dire_2, input_dire_3, input_dire_4, input_dire_5]

    #creating Label for each pick entry and putting them into LabelFrame grid
    for i in range(5):
        Label(dire_lf, text = ('Dire hero ' + str(i + 1) + ':')).grid(row = i+1, column = 0, sticky = W)
        dire_inputs[i].grid( row = i + 1, column = 1, padx = (20,0))

    #creating "Enter" button
    button_enter = Button(root, text = "Enter", command = read_text)

    #creating prediction label
    label_prediction = Label(root, text = '--prediction--')

    #putting both LabelFrames, button and prediction label into screen grid
    radiant_lf.grid(column=0, row=0, padx=20, pady=20, sticky = W)
    dire_lf.grid(column=0, row=1, padx=20, pady=20, sticky = W)
    button_enter.grid(column = 0, row = 2)
    label_prediction.grid(column = 0, row = 3)

    #mainloop
    root.mainloop()