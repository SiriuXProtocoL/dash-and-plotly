#/usr/bin/python3 -m pip install pip install  pandas pandas-datareader
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import datetime

#starting date
start = datetime.datetime(2015, 1, 1)
#till now
end = datetime.datetime.now()
#stock Name
stock = 'TSLA'

df = web.DataReader(stock, 'yahoo', start, end)

app = dash.Dash()

app.layout = html.Div(children = [
    html.H1("Live Stock"),
    dcc.Graph(id = 'example',
                figure = {'data' : [
                    {'x' : df.index, 'y' : df.Close, 'type' : 'line', 'name' : stock},
                    ], 'layout' : {'title' : stock}
                })
    ])

if __name__ == "__main__":
    app.run_server(debug=True)


#kill -9 $(ps -A | grep python | awk '{print $1}')
