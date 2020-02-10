import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import database as db

options = []

# query database for active candidates and put them in a dictionary
active_candidates = db.select_database("SELECT Candidate.name "
                                       + "FROM Candidate "
                                       + "WHERE date_dropped IS NULL")

# query database for all candidates and put them in the same dictionary
all_candidates = db.select_database("SELECT Candidate.name "
                                    + "FROM Candidate")

all_options = {
    'All Candidates': all_candidates['name'],
    'Active Candidates': active_candidates['name']
}



tab_4_layout = html.Div(
    [
        html.Div([
            dcc.Dropdown(
                id='active-dropdown',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='Active Candidates'
            ),
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='candidate-dropdown',
                placeholder="Select Candidate"
            ),
        ],
            style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Hr(),
        html.Div(id='display-candidate-overview')
    ]
)