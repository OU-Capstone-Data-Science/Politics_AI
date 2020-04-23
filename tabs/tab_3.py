import dash_core_components as dcc
import dash_html_components as html
from database import database as db

active_candidates = db.select_database("SELECT Candidate.name as [name], average_favorites, "
    + "average_retweets, average_tweets_per_day "
    + "FROM Candidate JOIN Twitter_Metrics ON Twitter_Metrics.name = Candidate.name "
    + "WHERE date_dropped IS NULL ")

all_candidates = db.select_database("SELECT Candidate.name as [name], average_favorites, "
    + "average_retweets, average_tweets_per_day "
    + "FROM Candidate JOIN Twitter_Metrics ON Twitter_Metrics.name = Candidate.name ")

all_options = {
    'All Candidates': all_candidates['name'],
    'Active Candidates': active_candidates['name']
}

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
                dcc.Dropdown(
                    id='active-dropdown-3',
                    options=[{'label': k, 'value': k} for k in all_options.keys()],
                    value='Active Candidates'
                ),
            ],
                style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='candidate-dropdown-3',
                    multi=True,
                    placeholder='Select candidate(s)'
                ),
            ],
                style={'width': '25%', 'display': 'inline-block'}
            ),
            html.Div([
            dcc.Dropdown(
                id='metric-dropdown-3',
                options=[{'label': 'Average Favorites Per Tweet', 'value': 'average_favorites'},
                         {'label': 'Average Retweets Per Tweet', 'value': 'average_retweets'},
                         {'label': 'Average Tweets Per Day', 'value': 'average_tweets_per_day'}
                         ],
                value='average_favorites',
                clearable=False
                ),
                ], style={'width': '25%', 'display': 'inline-block'}
            )
        ]),
        html.Div(id='display-selected-values-3'),
        dcc.Graph(id='box-graph-3', animate=True)
    ]
)