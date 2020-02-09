import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

tab_1_layout = html.Div(
    [html.H2('Live Twitter Sentiment'),
        dcc.Input(id='term', value='politics', type='text'),
        dcc.Graph(id='live-graph', animate=True),
        html.Div(id='tweets', children='Loading...', style={'display': 'block', 'margin-left': 'auto',
                                                            'margin-right': 'auto', 'text-align': 'center',
                                                            'width': 'fit-content'}),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)