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
                id='active-dropdown-4',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                value='Active Candidates'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='candidate-dropdown-4',
                placeholder='Select a candidate'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='policy-dropdown-4',
                options=[{'label': 'Overview', 'value': 'Overview'},
                         {'label': 'Endorsements', 'value': 'Endorsements'},
                         {'label': 'Agriculture', 'value': 'Agriculture'},
                         {'label': 'Campaign Finance', 'value': 'Campaign Finance'},
                         {'label': 'Childcare', 'value': 'Childcare'},
                         {'label': 'Criminal Justice Reform', 'value': 'Criminal Justice Reform'},
                         {'label': 'Drugs/Opioids', 'value': 'Drugs/Opioids'},
                         {'label': 'Education', 'value': 'Education'},
                         {'label': 'Environment', 'value': 'Environment'},
                         {'label': 'Foreign Policy', 'value': 'Foreign Policy'},
                         {'label': 'Government Shutdown', 'value': 'Government Shutdown'},
                         {'label': 'Gun Laws', 'value': 'Gun Laws'},
                         {'label': 'Healthcare', 'value': 'Healthcare'},
                         {'label': 'Housing', 'value': 'Housing'},
                         {'label': 'Immigration', 'value': 'Immigration'},
                         {'label': 'LGBT Rights', 'value': 'LGBT Rights'},
                         {'label': 'Minimum Wage', 'value': 'Minimum Wage'},
                         {'label': 'Net Neutrality', 'value': 'Net Neutrality'},
                         {'label': 'Trade', 'value': 'Trade'},
                         {'label': 'Veterans', 'value': 'Veterans'},
                         {'label': 'Women\'s Issues/Abortion', 'value': 'Women\'s Issues/Abortion'}],
                placeholder='Select a policy'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Br(),
        html.Br(),
        html.H1(id='title-4',
                style={'margin-right': 'auto',
                       'width': '75%'}
                ),
        html.Div(id='display-candidate-info-4',
                 style={'margin-right': 'auto',
                        'width': '75%'})
    ]
)
