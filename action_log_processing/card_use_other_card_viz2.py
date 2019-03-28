import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import numpy as np
import csv
from global_config import *
import os
from global_config import *

plotly.tools.set_credentials_file(username='shuoniu', api_key='dwCC2CLEvnYrO7gbbwpu')


def draw_plot(filename):
    id = filename.split('.')[0]
    points_x_ALEX = {}
    points_y_ALEX = {}
    points_x_CHRIS = {}
    points_y_CHRIS = {}

    with open(analysis_result + "\\card_position.csv") as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            if row['id'] == id:
                key = row['id'] + "_" + row['card name']
                if row['user'] == "ALEX":
                    if key not in points_x_ALEX:
                        points_x_ALEX[key] = []
                        points_y_ALEX[key] = []
                    if float(row['x']) > 640:
                        points_x_ALEX[key].append(float(row['x']))
                        points_y_ALEX[key].append(float(row['y']))
                if row['user'] == "CHRIS":
                    if key not in points_x_CHRIS:
                        points_x_CHRIS[key] = []
                        points_y_CHRIS[key] = []
                    if float(row['x']) < 640:
                        points_x_CHRIS[key].append(float(row['x']))
                        points_y_CHRIS[key].append(float(row['y']))

    data = []

    for tr in sorted(points_x_ALEX):
        trace = go.Scatter(
            x=points_x_ALEX[tr],
            y=points_y_ALEX[tr],
            mode='lines+markers',
            name=tr,
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=1)
        )
        data.append(trace)

    for tr in sorted(points_x_CHRIS):
        trace = go.Scatter(
            x=points_x_CHRIS[tr],
            y=points_y_CHRIS[tr],
            mode='lines+markers',
            name=tr,
            line=dict(
                color=('rgb(22, 96, 167)'),
                width=1)
        )
        data.append(trace)
    # print(data)
    return data


def draw_fig(data, name):
    layout = go.Layout(
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=True,
            showline=True,
            mirror='ticks',
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=4,
            linecolor='#636363',
            range=[0, 1280]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=True,
            showline=True,
            mirror='ticks',
            gridcolor='#bdbdbd',
            gridwidth=2,
            zerolinecolor='#969696',
            zerolinewidth=4,
            linecolor='#636363',
            scaleanchor='x',
            scaleratio=1,
            range=[720, 0]
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=name)


def process(directory):
    counter = 0
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            result = draw_plot(filename)
            draw_fig(result, filename.split(".")[0])
            continue
        else:
            continue


if __name__ == '__main__':
    process(processed_script_json)
