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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Politech'),
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


def generate_table(data_frame, term, max_rows=10):
    # Body
    rows = []
    for i in range(min(len(data_frame), max_rows)):
        row = []
        for col in data_frame.columns:
            sentiment = data_frame.iloc[i][1]
            style = cell_style(sentiment)
            row.append(html.Td(data_frame.iloc[i][col], style=style))
        rows.append(html.Tr(row))

    return html.Table(
        # Header
        [html.Tr([html.Th("Live twitter feed for the term \"" + term + "\"", style={'font-size': 'x-large'})])]
        + rows)


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

        return generate_table(last_ten, term)

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
def update_twitter_metrics(candidates, metric):
    data = None
    layout = None
    if candidates:
        name_list = list()
        metric_value_list = list()

        for name in candidates:
            query = "SELECT " + str(metric) + " FROM Twitter_Metrics " + "WHERE [name] = '" + str(name) + "'"
            data_table = db.select_database(query)

            name_list.append(name)
            metric_value_list.append(data_table[metric].values[0])

        data = go.Bar(
            x=name_list,
            y=metric_value_list,
            name='Bar'
        )

        layout = go.Layout(xaxis=dict(range=(0 - 1, len(name_list))),
                           yaxis=dict(range=[0, max(metric_value_list)]), )
    else:  # Use default data and layout
        data = {
            'x': [],
            'y': [],
            'type': 'bar'
        }

        layout = {
            'xaxis': {'title': 'Candidates'},
            'yaxis': {'title': metric},
            'barmode': 'relative',
            'title': metric
        }

    return {'data': [data], 'layout': layout}


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
# This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown', 'options'),
    [Input('active-dropdown', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]

# This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown', 'value'),
    [Input('candidate_dropdown', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']

# This callback sets a title based on the selected options in the three dropdowns
@app.callback(
    Output('title', 'children'),
    [Input('candidate-dropdown', 'value'),
     Input('policy-dropdown', 'value')])
def set_title(selected_candidate, selected_policy):
    if selected_policy == 'Overview':
        return "Overview of " + selected_candidate
    elif selected_policy == 'Endorsements':
        return selected_candidate + "'s 2020 presidential campaign endorsements"
    else:
        return selected_candidate + "'s views on " + selected_policy


# This callback displays the main body of text, scraped from wikipedia
@app.callback(
    Output('display-candidate-overview', 'children'),
    [Input('candidate-dropdown', 'value'),
     Input('policy-dropdown', 'value')])
def set_display_children(selected_candidate, selected_policy):
    # some smaller candidates may not have a positions page so we catch that error
    try:
        candidate_positions = wikipedia.page("Political positions of " + selected_candidate)
    except Exception as e:
        print(str(e))
    # try catch main page
    # try:
    #     candidate_main = wikipedia.page(selected_candidate)
    # except Exception as e:
    #     print(str(e))
    # # try catch for campaign page
    # try:
    #     candidate_campaign = wikipedia.page(selected_candidate + " 2020 presidential campaign")
    # except Exception as e:
    #     print(str(e))

    # lists of possible names for each section
    gun_laws = ["Gun laws", "Gun rights", "Gun control", "Gun Policy", "Guns", "Gun regulation"]
    # education = ["Education", "Higher education", "Education policy"]
    # campaign_finance = []
    # criminal_justice_reform = []
    # trade = []
    # gov_shutdown = []
    # lgbt_rights =[]
    # net_neutrality = []
    # immigration =[]
    # drugs = ["Drug Policy"]
    # agriculture = []
    # housing = []
    # environment = ["Environment"]

    if selected_policy == 'Overview':
        return wikipedia.summary(selected_candidate)
    elif selected_policy == 'Endorsements':
        # TODO make this prettier
        return wikipedia.page("List of " + selected_candidate + " 2020 presidential campaign endorsements").content()
    else:
        # small helper function to find the wikipedia page for the given position
        def find_policy(policy_name):
            # check the "political positions of" page first
            if candidate_positions:
                for option in policy_name:
                    if candidate_positions.section(option) is None:
                        continue
                        return "nope"
                    else:
                        return candidate_positions.section(option)
            # # next check their main page
            # elif candidate_main:
            #     for option in policy_name:
            #         if candidate_main.section(option) is None:
            #             continue
            #         else:
            #             return candidate_main.section(option)
            # # if that fails, check their campaign page (this is true for weld and yang)
            # elif candidate_campaign:
            #     for option in policy_name:
            #         if candidate_campaign.section(option) is None:
            #             continue
            #         else:
            #             return candidate_campaign.section(option)
            # if it's not on their main page either, print return an error message
            else:
                return "help"
                # no_policy = selected_candidate + " does not have an entry on Wikipedia for the policy of " + \
                #         selected_policy + "."
                # return no_policy

        if selected_policy == "Gun Laws":
            find_policy(gun_laws)
        # elif selected_policy == "Education":
        #     find_policy(education)
        # elif selected_policy == "Campaign Finance":
        #     find_policy(campaign_finance)
        # elif selected_policy == "Criminal Justice Reform":
        #     find_policy(criminal_justice_reform)
        # elif selected_policy == "Trade":
        #     find_policy(trade)
        # elif selected_policy == "Government Shutdown":
        #     find_policy(gov_shutdown)
        # elif selected_policy == "LGBT Rights":
        #     find_policy(lgbt_rights)
        # elif selected_policy == "Net Neutrality":
        #     find_policy(net_neutrality)
        # elif selected_policy == "Immigration":
        #     find_policy(immigration)
        # elif selected_policy == "Drugs/Opioids":
        #     find_policy(drugs)
        # elif selected_policy == "Agriculture":
        #     find_policy(agriculture)
        # elif selected_policy == "Housing":
        #     find_policy(housing)
        # elif selected_policy == "Environment":
        #     find_policy(environment)
        else:
            return "failed find_policy"


# Tab 5 callback
# Tab 5 callback
@app.callback(Output('line-graph', 'figure'),
              [Input('candidate-dropdown', 'value')])
def page_5_radios(candidates):
    try:
        lines = list()
        if candidates:
            print(candidates)
            for i in candidates:
                #query = "SELECT sentiment_date, ((positive_tweet_count * 1.) / " \
                #        + "(positive_tweet_count + negative_tweet_count + neutral_tweet_count)) * 100. as score" \
                query = "SELECT sentiment_date, compound_sentiment_vadersentiment * 100. as score" \
                        + " FROM Candidate_Sentiment" \
                        + " WHERE name = '" \
                        + str(i) \
                        + "';"

                dates = list()
                score = list()

                the_goods = db.select_database(query)

                for index, row in the_goods.iterrows():
                    dates.append(row['sentiment_date'])
                    score.append(row['score'])
                lines.append(plotly.graph_objs.Scatter(
                    x=np.asarray(dates),
                    y=np.asarray(score),
                    name=i,
                    mode='lines+markers'
                    ))
                print(lines)
            data = lines
            lines = list()
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (0-100%)'),
                          )

            return {'data': data, 'layout': layout}
        else:
            data = {
                'x': [],
                'y': [],
                'type': 'line'
            }
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (0-100%)'),
                          )
            return {'data': [data], 'layout': layout}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


# # TODO get better stylesheets
# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

if __name__ == '__main__':
    app.run_server(debug=True)
