#/usr/bin/python3 -m pip install pip install  pandas pandas-datareader
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas_datareader.data as web
import datetime

app = dash.Dash()

app.layout = html.Div(children = [

    html.Div(children='''
            Search a stock and we plot them:
            '''),
    dcc.Input(id="input", value='', type='text'),
    html.Div(id='output-graph')
    
    ])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_graph(input_data):
    #starting date
    start = datetime.datetime(2015, 1, 1)
    #till now
    end = datetime.datetime.now()

    df = web.DataReader(input_data, 'yahoo', start, end)

    #To graph
    return dcc.Graph(id = 'example',
                figure = {'data' : [
                    {'x' : df.index, 'y' : df.Close, 'type' : 'line', 'name' : input_data},
                    ], 'layout' : {'title' : input_data}
                })

if __name__ == "__main__":
    app.run_server(debug=True)


#kill -9 $(ps -A | grep python | awk '{print $1}')
