import dash_core_components as dcc
import dash_html_components as html
from database import database as db

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
        html.Br(),
        html.P('Select a candidate and a policy below to see their views on that policy.  All policy information is '
               'scraped directly from Wikipedia to ensure its accuracy.',
               style={'margin-right': 'auto',
                      'width': '66%'}
               ),
        html.Hr(),
        html.Div([
            dcc.Dropdown(
                id='active-dropdown',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='Active Candidates'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='candidate-dropdown',
                value='Amy Klobuchar'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='policy-dropdown',
                options=[{'label': 'Overview', 'value': 'Overview'},
                         {'label': 'Endorsements', 'value': 'Endorsements'},
                         {'label': 'Gun Laws', 'value': 'Gun Laws'},
                         {'label': 'Education', 'value': 'Education'},
                         {'label': 'Campaign Finance', 'value': 'Campaign Finance'},
                         {'label': 'Criminal Justice Reform', 'value': 'Criminal Justice Reform'},
                         {'label': 'Trade', 'value': 'Trade'},
                         {'label': 'Government Shutdown', 'value': 'Government Shutdown'},
                         {'label': 'LGBT Rights', 'value': 'LGBT Rights'},
                         {'label': 'Net Neutrality', 'value': 'Net Neutrality'},
                         {'label': 'Immigration', 'value': 'Immigration'},
                         {'label': 'Agriculture', 'value': 'Agriculture'},
                         {'label': 'Drugs/Opioids', 'value': 'Drugs/Opioids'},
                         {'label': 'Environment', 'value': 'Environment'},
                         {'label': 'Housing', 'value': 'Housing'}],
                value='Overview'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Br(),
        html.Br(),
        html.H1(id='title',
                style={'margin-right': 'auto',
                       'width': '75%'}
                ),
        html.Div(id='display-candidate-info',
                 style={'margin-right': 'auto',
                        'width': '75%'})
    ]
)
