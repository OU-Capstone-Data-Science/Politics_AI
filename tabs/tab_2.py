import dash_core_components as dcc
import dash_html_components as html

tab_2_layout = html.Div([
    html.Br(),
    html.P('Select a candidate below to see their recent polling data.'),
    html.Hr(),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    )
])

