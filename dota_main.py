import pickle
import pandas as pd
import json
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteEntry
from dota_ml import OH_encode


#creates pd dataframe from entry values and predicts value based on it
def read_text():

    #getting entry data from teams and picks entry widgets and combining them into a single array
    team_data = [int(input_radiant_teamid.get()), int(input_dire_teamid.get())]
    picks_data = [(entry.get()) for entry in (radiant_inputs + dire_inputs)]
    data = team_data + picks_data

    #creating pandas DataFrame with 1 row, based on entry values
    df = pd.DataFrame([data], columns=['radiant_team_id', 'dire_team_id', 'picks_radiant_1', 'picks_radiant_2', 'picks_radiant_3','picks_radiant_4',
                                      'picks_radiant_5 ', 'picks_dire_1', 'picks_dire_2', 'picks_dire_3', 'picks_dire_4', 'picks_dire_5'])

    #making a prediction from entry data
    prediction = ml_predict(df)

    #changing label text to show prediction value
    label_prediction.config(text = prediction)

#predicts outcome based on data by loading ml model
def ml_predict(data):
    #loading ml model
    model = pickle.load(open('finalized_model.sav', 'rb'))
    data = OH_encode(data)
    return model.predict(data)


#creating const hero array for autocomplete entries
HEROES = []
json_heroes = open('dota_heroes.json')
test_heroes = json.load(json_heroes)
for hero in test_heroes:
    HEROES.append(hero['name'])

#creating tkinter screen entity
root = Tk()
root.geometry('400x500')
root.title('Dota match predictions')

#creating LabelFrame for Radiant team
radiant_lf = LabelFrame(root, text = 'Radiant')

#creating team id Label and Entry and putting them into LabelFrame grid
Label(radiant_lf, text = 'Radiant team id').grid(row = 0, column = 0)
input_radiant_teamid = Entry(radiant_lf)
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
    Label(radiant_lf, text = ('Radiant hero ' + str(i + 1))).grid(row = i+1, column = 0, sticky = W)
    radiant_inputs[i].grid(row = i + 1, column = 1)

#creating LabelFrame for Dire team
dire_lf = LabelFrame(root, text = 'Dire')

#creating team id Label and Entry and putting them into LabelFrame grid
Label(dire_lf, text = 'Dire team id').grid(row = 0, column = 0)
input_dire_teamid = Entry(dire_lf)
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
    Label(dire_lf, text = ('Dire hero ' + str(i + 1))).grid(row = i+1, column = 0, sticky = W)
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
