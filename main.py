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
from database import database as db
import wikipedia
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Politech'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Live Sentiment Analysis', value='tab-1'),
        dcc.Tab(label='Polling Data', value='tab-2'),
        dcc.Tab(label='Twitter Metrics', value='tab-3'),
        dcc.Tab(label='Candidate Information & Policies', value='tab-4'),
        dcc.Tab(label='Sentiment Analysis Over Time', value='tab-5')
    ]),
    html.Div(id='tabs-content')
])


# DO NOT TOUCH
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab_1.tab_1_layout
    elif tab == 'tab-2':
        return tab_2.tab_2_layout
    elif tab == 'tab-3':
        return tab_3.tab_3_layout
    elif tab == 'tab-4':
        return tab_4.tab_4_layout
    elif tab == 'tab-5':
        return tab_5.tab_5_layout


# Tab 1 callback -- ALEX
@app.callback(Output('live-graph-1', 'figure'),
              [Input('term-1', 'value'), Input('graph-update-1', 'n_intervals')])
def update_graph_scatter(term, ignore):
    try:
        conn = sqlite3.connect(os.path.relpath('database/twitter.db'), check_same_thread=False, timeout=10.0)
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))
        if data_frame.empty:
            return {'data': [], 'layout': go.Layout(xaxis=dict(range=[-10, 10]),
                                                    yaxis=dict(range=[-10, 10]), )}
        # if the dataframe is not empty, update the graph
        else:
            data_frame.sort_values('unix', inplace=True)
            if int(len(data_frame)) < 5:
                rolling_value = 1
            else:
                rolling_value = int(len(data_frame) / 5)
            data_frame['sentiment_smoothed'] = data_frame['sentiment'].rolling(rolling_value).mean()
            data_frame.dropna(inplace=True)

            if int(len(data_frame)) < 100:
                data = go.Scatter(
                    x=data_frame.unix.values,
                    y=data_frame.sentiment_smoothed.values,
                    name='Scatter',
                    mode='lines+markers'
                )
                return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(data.x), max(data.x)], type='date'),
                                                            yaxis=dict(range=[min(data.y), max(data.y)]))}

            else:
                data = go.Scatter(
                    x=data_frame.unix.values[-100:],
                    y=data_frame.sentiment_smoothed.values[-100:],
                    name='Scatter',
                    mode='lines+markers'
                )
                return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(data.x), max(data.x)]),
                                                            yaxis=dict(range=[min(data.y), max(data.y)]))}


    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e) + ": tab 1 graph")
            error_file.write('\n')


@app.callback(Output('tweets-1', 'children'),
              [Input('term-1', 'value'), Input('graph-update-1', 'n_intervals')])
def update_tweets(term, ignore):
    try:
        conn = sqlite3.connect(os.path.relpath('database/twitter.db'), check_same_thread=False, timeout=10.0)
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))

        if data_frame.empty:
            return "There are currently no tweets about this term.  Wait for tweets to appear or select another term"
        else:
            data_frame.sort_values('unix', ascending=False, inplace=True)
            # get number of rows
            num_rows = int(len(data_frame))
            if num_rows < 10:
                last_ten = data_frame.iloc[:, 1:3]
            else:
                last_ten = data_frame.iloc[:10, 1:3]

            return generate_table(last_ten, term, num_rows)

    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e) + ": tab 1 tweets")
            error_file.write('\n')


# Tab 2 callback -- ERIC
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Tab 3 callbacks -- JACOB
# This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-3', 'options'),
    [Input('active-dropdown-3', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-3', 'value'),
    [Input('candidate_dropdown-3', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


@app.callback(Output('box-graph-3', 'figure'),
              [Input('candidate-dropdown-3', 'value'), Input('metric-dropdown-3', 'value')])
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
    Output('box-graph-3', 'layout'),
    [Input('candidate-dropdown-3', 'value'), Input('metric-dropdown-3', 'value')])
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


# Tab 4 callbacks -- ALEX (candidate overviews)
# This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-4', 'options'),
    [Input('active-dropdown-4', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-4', 'value'),
    [Input('candidate_dropdown-4', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# This callback sets a title based on the selected options in the three dropdowns
@app.callback(
    Output('title-4', 'children'),
    [Input('candidate-dropdown-4', 'value'),
     Input('policy-dropdown-4', 'value')])
def set_title(selected_candidate, selected_policy):
    if selected_policy == 'Overview' and selected_candidate is not None:
        return "Overview of " + selected_candidate
    elif selected_policy == 'Endorsements' and selected_candidate is not None:
        return selected_candidate + "'s 2020 presidential campaign endorsements"
    elif selected_candidate is not None and selected_policy is not None:
        return selected_candidate + "'s Views On " + selected_policy
    # if no values have been selected yet, return an empty string
    else:
        return ''


# This callback displays the main body of text, scraped from wikipedia
@app.callback(
    Output('display-candidate-info-4', 'children'),
    [Input('candidate-dropdown-4', 'value'),
     Input('policy-dropdown-4', 'value')])
def set_display_children(selected_candidate, selected_policy):
    # if no values have been selected yet, return an empty string
    if selected_candidate is None and selected_policy is None:
        return ""

    # append the values for Walsh and delaney
    if selected_candidate == "John Delaney":
        selected_candidate += " (Maryland politician)"
    if selected_candidate == "Joe Walsh":
        selected_candidate += " (American Politician)"

    # initialize page vars
    candidate_positions = None
    candidate_main = None
    candidate_campaign = None

    # some smaller candidates may not have a positions page so we catch that error
    try:
        candidate_positions = wikipedia.page("Political positions of " + selected_candidate)
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e) + ": tab 4 positions")
            f.write('\n')
    # if that fails, try catch main page
    if candidate_positions is None:
        try:
            candidate_main = wikipedia.page(selected_candidate)
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write(str(e) + ": tab 4 main")
                f.write('\n')
    # if that fails try catch for campaign page
    if candidate_positions is None and candidate_main is None:
        try:
            candidate_campaign = wikipedia.page(selected_candidate + " 2020 presidential campaign")
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write(str(e) + ": tab 4 campaign")
                f.write('\n')

    # lists of possible names for each section
    agriculture = ["Agriculture"]
    campaign_finance = ["Campaign finance reform", "Campaign finance"]
    childcare = ["Child care", "Family policy"]
    criminal_justice_reform = ["Criminal justice reform", "Criminal justice", "Stop-and-frisk"]
    drugs = ["Drug Policy", "Drug policy reform", "Drug laws"]
    education = ["Education", "Higher education", "Education policy"]
    environment = ["Environment", "Environmentalism", "Climate change and environment", "Climate change",
                   "Environmental policy"]
    foreign_policy = ["Foreign policy", "Foreign policy and national security", "Diplomacy"]
    gov_shutdown = ["2018–19 government shutdown"]
    gun_laws = ["Gun laws", "Gun rights", "Gun control", "Gun Policy", "Guns", "Gun regulation", "Gun law"]
    healthcare = ["Health care", "Healthcare", "Health insurance", "Health care policy"]
    housing = ["Housing"]
    immigration = ["Immigration", "Immigration policy", "Immigration on southern border"]
    lgbt_rights = ["LGBTQ+ rights", "LGBT rights", "LGBT issues"]
    minimum_wage = ["Minimum wage"]
    #marijuana = ["Cannabis legalization", "Cannabis"]
    net_neutrality = ["Net neutrality"]
    #opioids = ["Opioids"]
    trade = ["Trade"]
    veterans = ["Veterans Issues", "Veterans"]
    womens_issues_abortion = ["Women's issues and abortion", "Abortion"]

    if selected_candidate is not None:
        if selected_policy == 'Overview':
            return wikipedia.summary(selected_candidate, auto_suggest=False)
        elif selected_policy == 'Endorsements':
            # TODO make this prettier
            return wikipedia.page("List of " + selected_candidate + " 2020 presidential campaign endorsements").content
        else:
            if selected_policy is None:
                return ''
            elif selected_policy == "Agriculture":
                find_policy(agriculture, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Campaign Finance":
                find_policy(campaign_finance, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Childcare":
                find_policy(childcare, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Criminal Justice Reform":
                find_policy(criminal_justice_reform, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Drugs/Opioids":
                find_policy(drugs, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Education":
                find_policy(education, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Environment":
                find_policy(environment, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Foreign Policy":
                find_policy(foreign_policy, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Government Shutdown":
                find_policy(gov_shutdown, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Gun Laws":
                return find_policy(gun_laws, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Healthcare":
                find_policy(healthcare, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Housing":
                find_policy(housing, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Immigration":
                find_policy(immigration, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "LGBT Rights":
                find_policy(lgbt_rights, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Minimum Wage":
                find_policy(minimum_wage, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Marijuana":
                find_policy(marijuana, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Net Neutrality":
                find_policy(net_neutrality, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Opioids":
                find_policy(opioids, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Trade":
                find_policy(trade, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Veterans":
                find_policy(veterans, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Women's Issues/Abortion":
                find_policy(womens_issues_abortion, candidate_positions, candidate_main, candidate_campaign)
            else:
                return "There are no wikipedia entries available for this policy"


# tab 5 selection callbacks
# This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-5', 'options'),
    [Input('active-dropdown-5', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-5', 'value'),
    [Input('candidate_dropdown-5', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# Tab 5 main callback
@app.callback(Output('line-graph-5', 'figure'),
              [Input('candidate-dropdown-5', 'value')])
def page_5_radios(candidates):
    try:
        lines = list()
        if candidates:
            for i in candidates:
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
                          yaxis=dict(title='Sentiment Score -- (-100% - 100%)'),
                          )
            return {'data': [data], 'layout': layout}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e) + ": tab 5")
            f.write('\n')


# helper functions stored down here

# tab 1 update tweets helpers
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


def generate_table(data_frame, term, num_rows):
    # Body
    rows = []
    for i in range(min(num_rows, 10)):
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


# tab 4 helper
def find_policy(policy_name, candidate_positions, candidate_main, candidate_campaign):
    # check the "political positions of" page first
    if candidate_positions is not None:
        print("main")
        for option in policy_name:
            print(option)
            if candidate_positions.section(option) is None:
                continue
            else:
                return candidate_positions.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic
        print("no policy")
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy
    # next check their main page
    elif candidate_main is not None:
        print("main")
        for option in policy_name:
            print(option)
            if candidate_main.section(option) is None:
                continue
            else:
                return candidate_main.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic
        print("no policy")
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy
    # if that fails, check their campaign page (this is true for weld and yang)
    elif candidate_campaign is not None:
        print("campaign")
        for option in policy_name:
            print(option)
            if candidate_campaign.section(option) is None:
                continue
            else:
                return candidate_campaign.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic
        print("no policy")
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy
    # if it's not anywhere, print an error message
    else:
        no_candidate = "This candidate does not have an entry on Wikipedia."
        return no_candidate
        with open('errors.txt', 'a') as f:
            f.write("unable to find candidate anywhere")
            f.write('\n')


# tab 6 callbacks
# SELECT *
# FROM [Things].[dbo].[Candidate_Tweets]
# WHERE text LIKE '%health care%' AND [user_name] = 'Bernie Sanders'
def analyze_policy(selected_candidate, policy_input):
    return


if __name__ == '__main__':
    app.run_server(debug=True)
