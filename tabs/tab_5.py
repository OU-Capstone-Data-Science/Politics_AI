import dash_core_components as dcc
import dash_html_components as html

# formatted layout that describes the look and style of tab 5 using html wrappers
tab_5_layout = html.Div(
    html.Div([
        html.Br(),
        html.P('This graph represents poll data from the entirety of the 2020 Democratic Primary.  '
               'The data was web-scraped from RearClear Politics, and as such does not include Republican candidates, '
               'or candidates that dropped out earlier in the race.  Please allow time for the graphs to load - it '
               ' may take a moment to display the poll data due to the large amounts of information being graphed.',
               style={'margin-right': 'auto',
                      'width': '66%'}),
        html.Hr(),
        html.Div([
            # user can select their desired candidate here
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
        # line graph to isplay scraped poll data for the candidate in question
        dcc.Graph(id='line-graph-5', animate=True)
    ])
)
