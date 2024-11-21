import json
import os
from datetime import datetime
import numpy as np
import pandas as pd

from util import best_fit_slope_and_intercept

def count_votes(state):
    trump = 0
    biden = 0
    other = 0
    for r in state["results"]:
        votes = r["votes"]["count"]
        candidateID = r["candidateNpid"]
        if candidateID == 8639:
            trump += votes
        elif candidateID == 1036:
            biden += votes
        else:
            other += votes
    return trump, biden, other

def get_data_from_files(path, battlegrounds):
    totals = []
    file_names = os.listdir(path)
    for file_name in file_names:    
        time_stamp = datetime.fromtimestamp(float(file_name[7:-5]))
        file = open(path+file_name, 'r')
        results = json.loads(file.read())
        state_results = results["stateResults"]
        # Get Results from Files
        for state in state_results:
            state_code = state["stateCode"]
            if state_code in battlegrounds:

                (trump, biden, other) = count_votes(state)
                total = sum((trump, biden, other))
                percent = state["expectedPercentage"]

                poll = pd.Series({ 'Time' : time_stamp,
                                'State' : state_code,
                                'Progress' : percent / 100,
                                'Total' : total,
                                'Trump Share' : trump / total,
                                'Trump Vote' : trump,
                                'Biden Share' : biden / total,
                                'Biden Vote' : biden,
                                'Other Share' : other / total,
                                'Other Vote' : other})
                totals.append(poll)
    return totals

def predict_votes(dem_votes, rep_votes, progress):
    predict_x = 1
    m, b = best_fit_slope_and_intercept(progress,dem_votes)
    m2, b2 = best_fit_slope_and_intercept(progress,rep_votes)
    predict_dem = (m*predict_x)+b
    predict_rep = (m2*predict_x)+b2
    return predict_dem, predict_rep

def roll_dem(df):
    dem_votes = df['Biden Vote']
    rep_votes = df['Trump Vote']
    ys = df['Adjusted Progress']
    predict_dem, predict_rep = predict_votes(dem_votes, rep_votes, ys)
    return predict_dem

def roll_rep(df):
    dem_votes = df['Biden Vote']
    rep_votes = df['Trump Vote']
    ys = df['Adjusted Progress']
    predict_dem, predict_rep = predict_votes(dem_votes, rep_votes, ys)
    return predict_rep

def rolling_apply(df, period, func, min_periods=None):
    if min_periods is None:
        min_periods = period
    result = pd.Series(np.nan, index=df.index)

    for i in range(1, len(df)+1):
        sub_df = df.iloc[0:i,:] #I edited here
        if len(sub_df) >= min_periods:
            idx = sub_df.index[-1]
            result[idx] = func(sub_df)
    return result

def adjust_results(frame):
    adjusted = []
    for state_group in frame.groupby('State'):
        state_data = state_group[1]
        current_progress = state_data["Progress"].max()
        current_vote = state_data["Biden Vote"].max() + state_data["Trump Vote"].max() + state_data["Other Vote"].max()
        projected_total = current_vote * (1/current_progress)
        adjusted_progress = (state_data["Biden Vote"] + state_data["Trump Vote"] + state_data["Other Vote"]) / projected_total
        state_data["Adjusted Progress"] = adjusted_progress

        state_data["Biden Projection"] = rolling_apply(state_data, 50, roll_dem)
        state_data["Trump Projection"] = rolling_apply(state_data, 50, roll_rep)
        adjusted.append(state_data)

    return pd.concat(adjusted)

def build_results():
    folder_path = "./election-results/"
    battlegrounds = ["NV", "PA", "AZ", "GA"]
    data = get_data_from_files(folder_path, battlegrounds)
    data = pd.concat(data, axis=1).T
    data = adjust_results(data)
    data.to_csv('out.csv', index=False)  
