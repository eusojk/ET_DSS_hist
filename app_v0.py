import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers import make_dash_table, create_plot

from os import path # path
import os
import subprocess  #to run executable

# PLOTLY
import plotly_express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

port = int(os.environ.get("PORT", 5000))

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data").resolve()
url_csv = "https://raw.githubusercontent.com/SamEdwardes/dash-heroku-cookie-cutter/master/data/gapminder.csv"
# df = pd.read_csv(url_csv, index_col=0)

df = pd.read_csv(DATA_PATH.joinpath("small_molecule_drugbank.csv")).drop(
    ["Unnamed: 0"], axis=1
)

app.layout = html.Div(
    [
        html.Div(
            [html.Img(src=app.get_asset_url("SIMAGRI_CO_logo.gif"))], className="app__banner"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Climate-Agriculture Modeling Decision Support Tool for Ethiopia (Historical Analysis)",
                                    className="uppercase title",
                                ),
                                html.Span("CAMDT  ", className="uppercase bold"),
                                html.Span(
                                    "is a tool designed to guide decision-makers in adopting appropriate crop and management practices that can improve crop yields given a seasonal climatic condition."
                                ),
                                html.Br(),
                                html.Div(children='''
                                    Smart planning of annual crop production requires consideration of possible scenarios.
                                    The CAMDT tool adopts crop simulation models included in the DSSAT package (Decision Support System for Agrotechnology Transfer). 
                                    The methodology was developed by the IRI (International Research Institute for Climate and Society / Columbia University) 
                                    in collaboration with the Ethiopian Institute of Agricultural Research (EIAR). 
                                    The purpose of this tool is to support decision-making of the producer or technical advisor, which facilitates discussion of optimal production strategies, risks of technology adoption, 
                                    and evaluation of long-term effects, considering interactions of various factors.
                                '''),
                                html.Br(),
                                html.Span("Select ", className="uppercase bold"),
                                html.Span(
                                    "a station name for analysis."
                                ),
                            ]
                        )
                    ],
                    className="app__header",
                ),
        html.Div([
            html.Div(["Weather station: ",
                    dcc.Dropdown(id='mystation', options=[{'label': 'Bambey', 'value': 'CNRA'},{'label': 'Nioro', 'value': 'NRIP'},{'label': 'Sinthio', 'value': 'SNTH'}],
                    value='SNTH')]),
        html.H2(children='Period considered for the simulation:'),
            html.Div(["First year to simulate: ",
                    dcc.Input(id='year1', placeholder='Enter a value ...', value=' ', type='text')]),
            html.Div(["Last year to simulate: ",
                    dcc.Input(id='year2', placeholder='Enter a value ...', value=' ', type='text')]),
            html.Br(),

            html.Button(id='submit-button-state', n_clicks=0, children='Run DSSAT'),
            html.Div(id='output-state'),
            dcc.Graph(id='yield_boxplot'),
        ],style={'columnCount': 2}),
        # html.Div(id="number-output"),
    ]),
])

def update_experimental_file(file):
    line = "\n *** THIS FILE WAS MODIFIED WHILE RUNNING IN DOCKER. ***"
    with open(file, "a") as file_object:
        file_object.write(line)
    print('succ. modified')

# @app.callback(Output('yield_boxplot', 'figure'),
@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('mystation', 'value')])
def update_figure(n_clicks, input1):
    if n_clicks == 0:
        return dash.no_update

    print(input1)
    #1) make SNX
    dssat_files_dir = "dssat_files_dir/"
    temp_snx = path.join(dssat_files_dir, "SESGTEMP.SNX")
    snx_name = 'SESG'+input1+'.SNX'
    SNX_fname = path.join(dssat_files_dir, snx_name)
    fr = open(temp_snx, "r")  # opens temp SNX file to read
    fw = open(SNX_fname, "w")  # opens SNX file to write
    for i in range(20):
        temp_str = fr.readline()
        fw.write(temp_str)
    temp_str = fr.readline()
    new_str = temp_str[0:12] + input1 + temp_str[16:]  #replace weather station name
    fw.write(new_str)
    for i in range(41):
        temp_str = fr.readline()
        fw.write(temp_str)
    fw.close()
    fr.close()

    #2) Run DSSAT executable
    os.chdir(dssat_files_dir)  

    args = "./DSCSM047.EXE SGCER047 B DSSBatch.V47"
    os.system(args) 

    # go-back to parent directory
    parent = os.path.abspath(os.path.join(dssat_files_dir, os.pardir))
    os.chdir(parent) 

    #3) read DSSAT output


    #4) Make a boxplot
    # df = px.data.tips()
    # fig = px.box(df, x="time", y="total_bill")
    # fig.show()
    # fig.update_layout(transition_duration=500)

    # return create_plot(
    #     x=df["PKA"],
    #     y=df["LOGP"],
    #     z=df["SOL"],
    #     size=df["MW"],
    #     color=df["MW"],
    #     name=df["NAME"],
    # )

    return u'Selected station is  "{}" '.format(input1)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(debug=False,
                   host="0.0.0.0",
                   port=port)
