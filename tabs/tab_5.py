import dash_core_components as dcc
import dash_html_components as html
from database import database as db

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

tab_5_layout = html.Div(
    [
        html.Br(),
        html.P('Select a candidate or candidates to view and compare the average sentiment of their tweets each day.'
               '  A higher sentiment score means more positive tweets, and a lower score means more negative tweets.',
               style={'margin-right': 'auto',
                      'width': '66%'}),
        html.Hr(),
        html.Div([
            dcc.Dropdown(
                id='active-dropdown-5',
                options=[{'label': k, 'value': k} for k in all_options.keys()],
                placeholder='Select an option'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='candidate-dropdown-5',
                multi=True,
                placeholder='Select candidate(s)'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        html.Div(id='display-selected-values-5'),
        dcc.Graph(id='line-graph-5', animate=True)
    ]
)
