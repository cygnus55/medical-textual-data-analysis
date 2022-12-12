from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

from data_visualization import (fig_patient_gender, fig_patient_race, fig_allergy, fig_allergy_type,
                                fig_top_conditions, fig_cond_gender, fig_covid_21_22)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='Medical Data Visualization'),

    html.Div(children='''
        Some visualizations of medical data.
    '''),
    
    html.Hr(),
    
    html.H2(children='Patient Informations'),
    
    html.Div([
        html.Div([
            html.H4(children='Distribution of Gender'),


            dcc.Graph(
                id='graph1',
                figure=fig_patient_gender,
            ),  
        ], className='six columns'),
        html.Div([
            html.H4(children='Distribution of Race'),

            dcc.Graph(
                id='graph2',
                figure=fig_patient_race,
            ), 
        ], className='six columns'),
    ], className='row'),
    
    html.Hr(),
    
    html.H2(children='Allergies'),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='graph3',
                figure=fig_allergy,
            ),  
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='graph4',
                figure=fig_allergy_type,
            ), 
        ], className='six columns'),
    ], className='row'),
    
    html.Hr(),
    
    html.H2(children='Conditions'),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='graph5',
                figure=fig_top_conditions,
            ),  
        ], className='six columns'),
        html.Div([
            dcc.Graph(
                id='graph6',
                figure=fig_cond_gender,
            ), 
        ], className='six columns'),
    ], className='row'),
    
    html.Hr(),
    
    html.H2(children='Immunizations'),
    
    dcc.Graph(
        id='graph7',
        figure=fig_covid_21_22
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
