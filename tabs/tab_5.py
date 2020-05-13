import dash_core_components as dcc
import dash_html_components as html

tab_5_layout = html.Div(
    html.Div([
        html.Br(),
        html.P('This graph represents poll data from the entirety of the 2020 Democratic Primary.  '
               'The data was web-scraped from RearClear Politics, and as such does not include Republican candidates, '
               'or candidates that dropped out earlier in the race.',
               style={'margin-right': 'auto',
                      'width': '66%'}),
        html.Hr(),
        html.Div([
            dcc.Dropdown(
                id='candidate-dropdown-5',
                multi=True,
                options=[{'label': 'Joe Biden', 'value': 'Joe Biden'},
                         {'label': 'Bernie Sanders', 'value': 'Bernie Sanders'}],
                placeholder='Select candidate(s)'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        dcc.Graph(id='line-graph-5', animate=True)
    ])
)
