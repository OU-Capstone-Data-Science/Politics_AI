import dash_core_components as dcc
import dash_html_components as html

# poll_names = dberic.select_database("SELECT Poll FROM dbo.Polls")
# biden_poll_max = dberic.select_database("SELECT MAX(Biden) FROM dbo.Polls")
#
# poll_date = dberic.select_database("SELECT Date FROM dbo.Polls")
#
#
# poll_min_date = dberic.select_database(("SELECT MIN(Date) FROM dbo.Polls"))
# poll_max_date = dberic.select_database(("SELECT MAX(Date) FROM dbo.Polls"))
#
# candidate_biden = dberic.select_database("SELECT Biden FROM dbo.Polls")
# candidate_sanders = dberic.select_database("SELECT Sanders FROM dbo.Polls")
#
# tab_2_layout = html.Div(
#     html.Div([
#         html.Br(),
#
#         html.P('This graph represents poll data from the 2020 Democratic Presidential Nomination.'
#                'This data was web-scraped using BeautifulSoup from RearClear Politics.',
#                style={'margin-right': 'auto',
#                       'width' : '66%'}),
#
#         dcc.Graph(
#             id='example-graph-2',
#             figure={
#                 'data': [
#                     {'x': ["1/11/19", "2/23/19", "4/25/19", "5/03/19", "6/12/19", "8/14/19", "9/25/19", "11/02/19", "2/4/20"], 'y': [30, 28, 50, 45, 28, 35, 39, 42, 60], 'type': 'line', 'name': "Joe Biden"},
#                     {'x': ["1/11/19", "2/23/19", "4/25/19", "5/03/19", "6/12/19", "8/14/19", "9/25/19", "11/02/19", "2/4/20"], 'y': [25, 40, 15, 24, 20, 24, 20, 15, 19], 'type': 'line', 'name': "Bernie Sanders"},
#                 ],
#                 'layout': {
#                     'title': 'Poll Data Visualization',
#                     'xaxis' : dict(
#                         title='Date',
#                         titlefont=dict(
#                         family='Courier New, monospace',
#                         size=20,
#                         color='#7f7f7f'
#                     )),
#                     'yaxis' : dict(
#                         title='Poll Value',
#                         titlefont=dict(
#                         family='Helvetica, monospace',
#                         size=20,
#                         color='#7f7f7f'
#                     ))
#                 }
#             }
#         )
#
#     ])
# )

tab_2_layout = html.Div(
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
                id='candidate-dropdown-2',
                multi=True,
                options=[{'label': 'Joe Biden', 'value': 'Joe Biden'},
                         {'label': 'Bernie Sanders', 'value': 'Bernie Sanders'}],
                placeholder='Select candidate(s)'
            ),
        ],
            style={'width': '25%', 'display': 'inline-block'}
        ),
        dcc.Graph(id='line-graph-2', animate=True)
    ])
)
