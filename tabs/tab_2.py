import dash_core_components as dcc
import dash_html_components as html

tab_2_layout = html.Div([
    html.H1('Polling Data'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    )
])

