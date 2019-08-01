import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.graph_objs as go
import sqlite3

from collections import deque
from dash.dependencies import Input, Output

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
stock ='TSLA'



app = dash.Dash('Kosovo-Tweet-Sentiment')
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False


app.layout = html.Div(
    [
        html.Div([
            html.H3('Analize e Sentimentit ne Twitter',
                    style = {'float': 'center',

                    })
        ]),
        dcc.Input(id='input-1-keypress',
                     type='text',
                     value='Shtepia',
                  style = {}
                     ),
        html.Div(children=html.Div(id='graphs'), className='row'),
        dcc.Interval (
            id='graph-update',
            interval=1000,
            n_intervals=0
        )
    ], className="container", style={'width':'98%', 'margin-left':10, 'margin-right':10, 'max-width':50000}

)

@app.callback(Output('graphs', 'children'),
[Input('input-1-keypress', 'value'), Input('graph-update', '')],
              )
def update_graph(data_names, n_interval):

    conn = sqlite3.connect('/Users/adrianasejfia/PycharmProjects/TwitterSentimentAnalysis/TwitterSentimentAnalysis/twitter.db')
    c = conn.cursor()
    query_param = '%' + data_names + '%'
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE :who", con=conn, params={"who":query_param})


    df.sort_values('unix', inplace=True)
    X = df.unix.values[-100:]
    Y = df.sentiment.values[-100:]


    graphs = []

    if len(list(X)) == 0:
        X = [0]
        graphs.append(html.Div([html.H4("Fjala nuk ekziston ne databaze.")]))
        return graphs

    if len(list(Y)) == 0:
        Y = [0]
        graphs.append(html.Div([html.H4("Fjala nuk ekziston ne databaze.")]))
        return graphs

    class_choice = 'col s12 m6 14'

    data = go.Scatter(
            x = list(X),
            y = list(Y),
            name = 'twitter sentiment analysis',
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




    return graphs

external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']
for css in external_css:
    app.css.append_css({"external_url":css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.5/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})


if __name__ == "__main__":
    app.run_server(debug=True)