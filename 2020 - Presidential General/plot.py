import pandas as pd
import matplotlib.pyplot as plt
from util import calculate_regression

def build_plot(data):
    battlegrounds = list(data.groupby('State').groups)
    fig, axs = plt.subplots(len(battlegrounds), 5)

    plt.style.use('fivethirtyeight') # For better style
    fig.tight_layout()

    color_dem = '#0000FF'
    color_rep = '#FF0000'
    color_pred_dem = '#AAAAFF'
    color_pred_rep = '#FFAAAA'

    for state_group in data.groupby('State'):
        state_data = state_group[1]
        state_code = state_group[0]

        dem_votes = state_data['Biden Vote']
        rep_votes = state_data['Trump Vote']
        ys = state_data['Adjusted Progress']

        regression_line_dem = calculate_regression(dem_votes, ys)
        regression_line_rep = calculate_regression(rep_votes, ys)

        (ax1, ax2, ax3, ax4, ax5) = axs[battlegrounds.index(state_code)]

        #Scatter
        ax1.scatter(ys,dem_votes,color=color_dem,label='data')
        ax1.scatter(ys,rep_votes,color=color_rep,label='data')
        ax1.plot(regression_line_dem, dem_votes, color=color_pred_dem, label='regression line')
        ax1.plot(regression_line_rep, rep_votes, color=color_pred_rep, label='regression line')
        ax1.title.set_text(state_code + ' Scatter Vote')

        #Votes v Progress
        state_data.plot(ax = ax2, y=['Biden Vote', 'Trump Vote'], color=[color_dem, color_rep], x='Adjusted Progress', legend=None)
        ax2.plot(regression_line_dem,dem_votes, color=color_pred_dem, label='regression line')
        ax2.plot(regression_line_rep,rep_votes, color=color_pred_rep, label='regression line')
        ax2.title.set_text(state_code + ' Vote of Reporting')

        #Votes over Time
        state_data.plot(ax = ax3, y=['Biden Vote', 'Trump Vote'], color=[color_dem, color_rep],x='Time', legend=None)
        ax3.title.set_text(state_code + ' Vote Over Time')

        #Share over Time
        state_data.plot(ax = ax4, y=['Biden Share', 'Trump Share'], color=[color_dem, color_rep],x='Adjusted Progress', legend=None)
        ax4.title.set_text(state_code + ' Share of Reporting')

        #Projection over Time
        state_data.plot(ax = ax5, y=['Biden Projection', 'Trump Projection'], color=[color_dem, color_rep],x='Time', legend=None)
        ax5.title.set_text(state_code + ' Projection Over Time')
