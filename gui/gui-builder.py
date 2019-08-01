import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.graph_objs as go
import random
import sqlite3
import time

from collections import deque
from dash.dependencies import Input, Output, State

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
stock ='TSLA'



app = dash.Dash('Kosovo-Tweet-Sentiment')

max_length = 20
times = deque(maxlen=max_length)
oil_temps = deque(maxlen=max_length)
intake_temps = deque(maxlen=max_length)
coolant_temps = deque(maxlen=max_length)
rpms = deque(maxlen=max_length)
speeds = deque(maxlen=max_length)
throttle_pos = deque(maxlen=max_length)

data_dict = {"Kosovo":"Kosovo",
             "Politika": "Politika",
             "Temperatura": "Temperatura",
}


def update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throtte_pos):
    times.append(time.time())
    if len(times) == 1:
        oil_temps.append(random.randrange(180, 230))
        intake_temps.append(random.randrange(95, 115))
        coolant_temps.append(random.randrange(170, 220))
        rpms.append(random.randrange(1000, 9500))
        speeds.append(random.randrange(30, 140))
        throttle_pos.append(random.randrange(10, 90))
    else:
        for data_of_interest in [oil_temps, intake_temps, coolant_temps, rpms, speeds, throtte_pos]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001, 0.0001))
    return times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throtte_pos

# times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos = update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)


app.layout = html.Div(
    [
        html.Div([
            html.H2('Kosovo Tweets Sentiment Analysis',
                    style = {'float': 'left',
                    })
        ]),
        dcc.Input(id='input-1-keypress',
                     type='text',
                     value='Shtepia',
                     ),
        html.Div(children=html.Div(id='graphs'), className='row'),
        dcc.Interval (
            id='graph-update',
            interval=1000,
            n_intervals=0
        )
    ], className="container", style={'width':'98%', 'margin-left':10, 'margin-right':10, 'max-width':50000}
    # [
    # dcc.Graph(id='live-graph', animate=True),
    # dcc.Interval(
    #     id='graph-update',
    #     interval = 1000
    # )
    # ]
    # children=[
    # html.Div(children='''
    #     Dash: A web application framework for Python.
    # '''),
    # dcc.Input(id='input', value='', type='text'),
    # html.Div(id='output-graph')
    # ]
)

@app.callback(Output('graphs', 'children'),
[Input('input-1-keypress', 'value'), Input('graph-update', '')],
              )
def update_graph(data_names, n_interval):
    print(data_names)
    conn = sqlite3.connect('C:\\Users\\asejfia\\Desktop\\TweetStreamer\\TwitterSentimentAnalysis\\twitter.db')
    c = conn.cursor()
    query_param = '%' + data_names + '%'
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE :who", con=conn, params={"who":query_param})
    # df = (conn.execute("SELECT * FROM sentiment WHERE tweet LIKE :who ORDER BY unix DESC LIMIT 100",  {"who":'%Shtepia%'}))



    X = df.unix.values[-100:]
    Y = df.sentiment.values[-100:]
    print(df)

    print("X")
    print(X)

    print("Y")
    print(Y)

    graphs = []

    if len(list(X)) == 0:
        X = [0]
        graphs.append(html.Div([html.H1("Fjala nuk ekziston ne databaze.")]))
        return graphs

    if len(list(Y)) == 0:
        Y = [0]
        graphs.append(html.Div([html.H1("Fjala nuk ekziston ne databaze.")]))
        return graphs

    if len(data_names)>2:
        class_choice = 'col s12 m6 14'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 16'
    else:
        class_choice = 'col s12'

    # for data_name in data_names:
    data = go.Scatter(
            x = list(X),
            y = list(Y),
            name = 'ski',
            fill = "tozeroy",
            fillcolor = "#6897bb"
        )

    graphs.append(html.Div(dcc.Graph(
            id=data_names,
            animate=True,
            figure={'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                        yaxis=dict(range=[min(Y),
                                                                          max(Y)]),
                                                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                                                        title='{}'.format(data_names))}
        ), className=class_choice))

    print("graphs")
    print(graphs)

    return graphs

external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']
for css in external_css:
    app.css.append_css({"external_url":css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/css/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})
# def update_graph_scatter(n):
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
#
#     data = plotly.graph_objs.Scatter(
#         x=list(X),
#         y=list(Y),
#         name = 'Scatter',
#         mode = 'lines+markers'
#     )
#
#     return {'data':[data], 'layout': go.Layout(xaxis = dict(range=[min(X), max(X)]),
#                                                yaxis = dict(range=[min(Y), max(Y)]))}
# @app.callback(
#     Output(component_id='output-graph', component_property='children'),
#     [Input(component_id='input', component_property='value')])
#
#
# def update_graph(input_data):
#     start = datetime.datetime(2015, 1, 1)
#     end = datetime.datetime(2018, 2, 8)
#     df = web.get_data_yahoo(input_data, start, end)
#
#     return dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
#             ],
#             'layout': {
#                 'title': input_data
#             }
#         }
#     )
# def update_value(input_data):
#     try:
#         return str(float(input_data)**2)
#     except:
#             return "Some error"

if __name__ == "__main__":
    app.run_server(debug=True)