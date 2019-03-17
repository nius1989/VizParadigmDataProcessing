import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy
import csv

plotly.tools.set_credentials_file(username='shuoniu', api_key='dwCC2CLEvnYrO7gbbwpu')

matrix = []

with open("D:\\viz_data_8\\final_result\\heat_map\\matrix_MEG.csv", "rt") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        matrix.append(list(map(float, row)))

trace = go.Heatmap(z=matrix)
data = [trace]
py.plot(data, filename='basic-heatmap')
