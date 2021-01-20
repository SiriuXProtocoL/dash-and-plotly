import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd
import time


app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Twitter Sentiment'),
        #dynamic input with default input
        dcc.Input(id='sentiment_term', value='stock', type='text'),
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),

    ]
)

@app.callback(Output('live-graph', 'figure'),
                #the component id is the term and the property is the value of dynamic input
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')])
def update_graph_scatter(sentiment_term):
    try:
        #connection
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()

        #this pandas menthod allows to trim and adjust the user serach
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn ,params=('%' + sentiment_term + '%',))
        df.sort_values('unix', inplace=True)

        #to make the x and y ticks readable manipulate the date
        df['date'] = pd.to_datetime(df['unix'],unit='ms')
        df.set_index('date', inplace=True)

        #moving average
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()


        df.dropna(inplace=True)

        #makes the data visualation easy to read
        #paly around with this
        df = df.resample('3000ms').mean()

        #defining the x and y
        X = df.index[-100:]
        Y = df.sentiment_smoothed.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    title='Term: {}'.format(sentiment_term))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

if __name__ == '__main__':
    app.run_server(debug=True)