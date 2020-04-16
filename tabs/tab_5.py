import dash_core_components as dcc
import dash_html_components as html
from database import database as db

candidates = db.select_database("SELECT Candidate.name as [name] "
                                + "FROM Candidate"
                                + " WHERE Candidate.date_dropped IS NULL")
all_candidates = {
    'candidates': candidates['name']
}

tab_5_layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='candidate-dropdown',
            options=[{'label': i, 'value': i} for i in all_candidates['candidates']],
            multi=True,
            placeholder="Select Candidates"
            ),
            ],
            style={'width': '50%', 'display': 'inline-block'}),
        html.Hr(),
        html.Div(id='display-selected-values'),
        dcc.Graph(id='line-graph', animate=True)
    ]
)