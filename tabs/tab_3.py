import dash_core_components as dcc
import dash_html_components as html
from database import database as db

candidates = db.select_database("SELECT Candidate.name as [name], average_favorites, "
    + "average_retweets, average_tweets_per_day "
    + "FROM Candidate JOIN Twitter_Metrics ON Twitter_Metrics.name = Candidate.name "
    + "WHERE date_dropped IS NULL ")
all_candidates = {
    'candidates': candidates['name']
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
        dcc.Dropdown(
            id='candidate-dropdown',
            options=[{'label': i, 'value': i} for i in all_candidates['candidates']],
            multi=True,
            placeholder="Select Candidate(s)"
            ),
            ],
            style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': 'Average Favorites Per Tweet', 'value': 'average_favorites'},
                     {'label': 'Average Retweets Per Tweet', 'value': 'average_retweets'},
                     {'label': 'Average Tweets Per Day', 'value': 'average_tweets_per_day'}
                     ],
            value='average_favorites',
            clearable=False
            ),
            ], style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Div(id='display-selected-values'),
        dcc.Graph(id='box-graph', animate=True)
    ]
)