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

# dictionary containing active and all candidates
all_options = {
    'All Candidates': all_candidates['name'],
    'Active Candidates': active_candidates['name']
}

# formatted layout that describes the look and style of tab 6 using html wrappers
tab_6_layout = html.Div([
    html.Br(),
    html.P('Select a candidate and a popular topic below to see the average sentiment of their tweets on that topic.'),
    html.Hr(),
    html.Div([
        # allows for the user to select active or all candidates
        dcc.Dropdown(
            id='active-dropdown-6',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            placeholder='Select an option'
        ),
    ],
        style={'width': '25%', 'display': 'inline-block'}
    ),
    html.Div([
        # user selects candidate(s) they'd like to display here
        dcc.Dropdown(
            id='candidate-dropdown-6',
            placeholder='Select a candidate'
        ),
    ],
        style={'width': '25%', 'display': 'inline-block'}
    ),
    html.Hr(),
    html.P('Enter a search term: '),
    # allows user to input any search term they want
    dcc.Input(id='input-6', value='health care', type='text'),
    html.Br(),
    # number of tweets for the relevant search term is displayed here
    html.Div(id='num-tweets-6'),
    # average sentiment for the relevant search term is displayed here
    html.Div(id='sentiment-6'),
    # all tweets for the relevant search term are displayed here
    html.Div(id='tweets-list-6', style={'white-space': 'pre-wrap'})
])