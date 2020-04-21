import dash_core_components as dcc
import dash_html_components as html

tab_6_layout = html.Div([
    html.Br(),
    html.P('Select a candidate and a popular topic below to see the average sentiment of their tweets on that topic.'),
    html.Hr(),
    dcc.Input(id='topic', value='health care', type='text'),
    html.Div('Number of tweets will go here'),
    html.Div('Average Sentiment will go here'),
    html.Br(),
    html.Div('Individual tweets will go here in a scrolling list')
])