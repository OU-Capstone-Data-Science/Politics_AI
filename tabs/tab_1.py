import dash_core_components as dcc
import dash_html_components as html

# formatted layout that describes the look and style of tab 1 using html wrappers
tab_1_layout = html.Div(
    [
        html.Br(),
        html.P('This chart displays live sentiment analysis data from twitter about the chosen search term.  Tweets are'
               ' analyzed as they come in, their sentiment value appears on the graph above, and the tweets scroll '
               'below.  Red tweets have negative language, green tweets have positive language, and yellow are neutral.',
               style={'margin-right': 'auto',
                      'width': '66%'}),
        html.Hr(),
        html.P('Enter a search term: '),
        dcc.Input(id='term-1', value='trump', type='text'),
        # contains graphed sentiment scores from our sqlite db
        dcc.Graph(id='live-graph-1', animate=True, figure={'data': [], 'layout': {}}),
        # this div contains the text of the tweets read in from our sqlite db
        html.Div(id='tweets-1', children='Loading...', style={'margin-left': 'auto',
                                                              'margin-right': 'auto',
                                                              'text-align': 'center',
                                                              'width': 'fit-content'}),
        # used to determine how often to update the graph
        dcc.Interval(
            id='graph-update-1',
            interval=1 * 1000
        ),
    ]
)
