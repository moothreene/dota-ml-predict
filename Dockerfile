FROM python:3.8

ADD main.py dota_preprocess_initial.py dota_ml.py finalized_model.sav dota_heroes.json dota_majors.json dota_winrates_by_hero.json dota_teams.json ./

RUN pip install pandas scikit-learn tensorflow keras

CMD [ "python", "./main.py" ]