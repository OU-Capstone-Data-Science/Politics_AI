import dash_core_components as dcc
import dash_html_components as html
from database import database as db

# gets twitter data for active candidates
active_candidates = db.select_database("SELECT Candidate.name as [name], average_favorites, "
    + "average_retweets, average_tweets_per_day "
    + "FROM Candidate JOIN Twitter_Metrics ON Twitter_Metrics.name = Candidate.name "
    + "WHERE date_dropped IS NULL ")

# gets twitter data for all candidates
all_candidates = db.select_database("SELECT Candidate.name as [name], average_favorites, "
    + "average_retweets, average_tweets_per_day "
    + "FROM Candidate JOIN Twitter_Metrics ON Twitter_Metrics.name = Candidate.name ")

# dictionary to hold inactive and all candidates
all_options = {
    'All Candidates': all_candidates['name'],
    'Active Candidates': active_candidates['name']
}

# formatted layout that describes the look and style of tab 3 using html wrappers
tab_3_layout = html.Div(
    [
        html.Br(),
        html.P('Select a candidate or candidates to view and compare their average likes, average favorites, and '
               'average retweets.',
               style={'margin-right': 'auto',
                       'width': '66%'}),
        html.Hr(),
        html.Div([
            html.Div([
                # allows for the user to select active or all candidates
                dcc.Dropdown(
                    id='active-dropdown-3',
                    options=[{'label': k, 'value': k} for k in all_options.keys()],
                    placeholder='Select an option'
                ),
            ],
                style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                # user selects candidate(s) they'd like to display here
                dcc.Dropdown(
                    id='candidate-dropdown-3',
                    multi=True,
                    placeholder='Select candidate(s)'
                ),
            ],
                style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                # user can select which metric they would like to display here
                dcc.Dropdown(
                    id='metric-dropdown-3',
                    options=[{'label': 'Average Favorites Per Tweet', 'value': 'average_favorites'},
                             {'label': 'Average Retweets Per Tweet', 'value': 'average_retweets'},
                             {'label': 'Average Tweets Per Day', 'value': 'average_tweets_per_day'}
                             ],
                    value='average_favorites',
                    clearable=False
                ),
            ],
                style={'width': '25%', 'display': 'inline-block'}
            )
        ]),
        # bar graph diplaying selected twitter metrics
        dcc.Graph(id='box-graph-3', animate=True)
    ]
)