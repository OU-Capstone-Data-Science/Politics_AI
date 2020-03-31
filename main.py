import os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly
import plotly.graph_objs as go
from tabs import tab_1, tab_2, tab_3, tab_4, tab_5
from tabs.tab_4 import all_options
import pandas as pd
import sqlite3
import database as db
import wikipedia

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Boys Rule'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Live Sentiment Analysis', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
        dcc.Tab(label='Twitter Metrics', value='tab-3-example'),
        dcc.Tab(label='Candidate Information & Policies', value='tab-4-example'),
        dcc.Tab(label='Tab Five', value='tab-5-example')
    ]),
    html.Div(id='tabs-content-example')
])


# DO NOT TOUCH
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1.tab_1_layout
    elif tab == 'tab-2-example':
        return tab_2.tab_2_layout
    elif tab == 'tab-3-example':
        return tab_3.tab_3_layout
    elif tab == 'tab-4-example':
        return tab_4.tab_4_layout
    elif tab == 'tab-5-example':
        return tab_5.tab_5_layout


# Tab 1 callback -- ALEX
@app.callback(Output('live-graph', 'figure'),
              [Input('term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_scatter(term, ignore):
    try:
        conn = sqlite3.connect(os.path.relpath('jacob_duvall/twitter.db'))
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))
        data_frame.sort_values('unix', inplace=True)
        rolling_value = int(len(data_frame) / 5)
        data_frame['sentiment_smoothed'] = data_frame['sentiment'].rolling(rolling_value).mean()
        data_frame.dropna(inplace=True)

        data = go.Scatter(
            x=data_frame.unix.values[-100:],
            y=data_frame.sentiment_smoothed.values[-100:],
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(data.x), max(data.x)]),
                                                    yaxis=dict(range=[min(data.y), max(data.y)]), )}

    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e))
            error_file.write('\n')


@app.callback(Output('tweets', 'children'),
              [Input('term', 'value'), Input('graph-update', 'n_intervals')])
def update_tweets(term, ignore):
    try:
        conn = sqlite3.connect(os.path.relpath('jacob_duvall/twitter.db'))
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))
        data_frame.sort_values('unix', ascending=False, inplace=True)
        last_ten = data_frame.iloc[:10, 1:3]

        def cell_style(value):
            # color the text of negative values red
            if value < 0:
                style = {'color': '#d11919'}
            # color the text of positive values green
            elif value > 0:
                style = {'color': '#19d119'}
            # color neutral (0 sentiment value) values yellow
            else:
                style = {'color': '#e6cd12'}
            return style

        def generate_table(dataframe, max_rows=10):

            # Body
            rows = []
            for i in range(min(len(dataframe), max_rows)):
                row = []
                for col in dataframe.columns:
                    sentiment = dataframe.iloc[i][1]
                    style = cell_style(sentiment)
                    row.append(html.Td(dataframe.iloc[i][col], style=style))
                rows.append(html.Tr(row))

            return html.Table(
                # Header
                [html.Tr([html.Th("Live twitter feed for the term \"" + term + "\"", style={'font-size': 'x-large'})])]
                + rows)

        return generate_table(last_ten)

    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e))
            error_file.write('\n')


# Tab 2 callback -- ERIC
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Tab 3 callback -- JACOB
@app.callback(Output('box-graph', 'figure'),
              [Input('candidate-dropdown', 'value'), Input('metric-dropdown', 'value')])
def page_3_booyah(candidates, metric):
    guys = list()
    gals = list()
    rule = list()
    if candidates:
        for i in candidates:
            query = "SELECT " + str(metric) + " FROM Twitter_Metrics " + "WHERE [name] = '" + str(i) + "'"
            the_goods = db.select_database(query)

            guys.append(i)
            gals.append(the_goods[metric].values[0])

        data = plotly.graph_objs.Bar(
            x=guys,
            y=gals,
            name='Bar'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=(0 - 1, len(guys))),
                                                    yaxis=dict(range=[0, max(gals)]), )}

    all_info_baby = {
        'x': [],
        'y': [],
        'type': 'bar'
    }
    layout = {
        'xaxis': {'title': 'Candidates'},
        'yaxis': {'title': metric},
        'barmode': 'relative',
        'title': metric
    };
    rule.append(all_info_baby)

    return {'data': rule, 'layout': layout}


@app.callback(
    Output('box-graph', 'layout'),
    [Input('candidate-dropdown', 'value'), Input('metric-dropdown', 'value')])
def label_axes(candidates, metric):
    if candidates:
        versus = ''
        for candidate in candidates:
            versus += candidate + " vs. "
        versus = versus[0:-4]
        layout = {
            'xaxis': {'title': versus},
            'yaxis': {'title': metric},
            'barmode': 'relative',
            'title': metric
        };
        print(layout)


# Tab 4 callbacks -- ALEX (candidate overviews)
@app.callback(
    Output('candidate-dropdown', 'options'),
    [Input('active-dropdown', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


@app.callback(
    Output('candidate-dropdown', 'value'),
    [Input('candidate_dropdown', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-candidate-overview', 'children'),
    [Input('candidate-dropdown', 'value'),
     Input('policy-dropdown', 'value')])
def set_display_children(selected_candidate, selected_policy):
    candidate_page = wikipedia.page("Political positions of " + selected_candidate)
    if selected_policy == 'Overview':
        return wikipedia.summary(selected_candidate)
    elif selected_policy == 'Endorsements':
        # TODO make this prettier
        return wikipedia.page("List of " + selected_candidate + " 2020 presidential campaign endorsements").content
    else:
        # TODO either figure out how to get these sections out or write scrapers for all candidates
        return candidate_page.sections


# Tab 5 callback
@app.callback(Output('page-5-content', 'children'),
              [Input('page-5-radios', 'value')])
def page_5_radios(value):
    return 'You have selected "{}"'.format(value)


# TODO get better stylesheets
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
