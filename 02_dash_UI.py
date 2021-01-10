import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children = [
    #creating an input field
    dcc.Input(id = 'input', value='Enter a value', type='text'),
    #assign id for the generated output
    html.Div(id='output')
    ])

#function to handle the input and produce the output
@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    return str(float(input_data)**2)
    #return "Input : {}".format(input_data)

if __name__ == "__main__":
    app.run_server(debug=True)