import os
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly
import plotly.graph_objs as go
from tabs import tab_1, tab_5, tab_3, tab_4, tab_2, tab_6
from tabs.tab_4 import all_options
import pandas as pd
import sqlite3
from database import database as db
from database import database_eric as dberic
import wikipedia
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# import the base Dash stylesheets for use when initializing our Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# initialize the app with the given stylesheets and set its title
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = "Politech"

# keep the app from throwing callback exceptions for a cleaner user experience
app.config.suppress_callback_exceptions = True

# set framework for app layout by establishing 6 tabs, to be used in the next callback
app.layout = html.Div([
    html.H1('Politech'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Live Sentiment Analysis', value='tab-1'),
        dcc.Tab(label='Sentiment Analysis Over Time', value='tab-2'),
        dcc.Tab(label='Twitter Metrics', value='tab-3'),
        dcc.Tab(label='Candidate Information & Policies', value='tab-4'),
        dcc.Tab(label='Polling Data', value='tab-5'),
        dcc.Tab(label='Candidate Sentiment on Specific Topics', value='tab-6')
    ]),
    # this is what will be updated by the next callback
    html.Div(id='tabs-content')
])


# return the appropriate tab layout from the tab_#.py files
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
    elif tab == 'tab-6':
        return tab_6.tab_6_layout


# Tab 1 -- update line graph as new tweet data comes in
@app.callback(Output('live-graph-1', 'figure'),
              [Input('term-1', 'value'), Input('graph-update-1', 'n_intervals')])
# interval value isn't used in function but is needed so graph updates regularly
def update_graph_scatter(term, interval):
    try:
        # establish connection to the sqlite3 db
        conn = sqlite3.connect(os.path.relpath('database/twitter.db'), check_same_thread=False, timeout=10.0)
        # perform a search on the db based on our given term and load the results into a dataframe
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))

        # this will only execute on the first callback after the database has been deleted
        # the user will likely never encounter this, and if they do it will only be for one second
        if data_frame.empty:
            return {'data': [], 'layout': go.Layout(xaxis=dict(range=[-10, 10]),
                                                    yaxis=dict(range=[-10, 10]), )}

        # if the dataframe is not empty, update the graph
        else:
            # sort values by their unix time value, then get a rolling average of their sentiment scores
            data_frame.sort_values('unix', inplace=True)
            if int(len(data_frame)) < 5:
                rolling_value = 1   # helps with rolling average if we have very few values
            else:
                rolling_value = int(len(data_frame) / 5)
            data_frame['sentiment_smoothed'] = data_frame['sentiment'].rolling(rolling_value).mean()
            # gets rid of stray NaN values, if any exist
            data_frame.dropna(inplace=True)

            # if we have less than 100 tweets, load them all into the graph
            if int(len(data_frame)) < 100:
                data = go.Scatter(
                    x=data_frame.unix.values,                   # x axis is datetime
                    y=data_frame.sentiment_smoothed.values,     # y axis is sentiment
                    name='Scatter',
                    mode='lines+markers'
                )
                # returns a Plotly Figure, with the data we set earlier and the datetime formatted as calendar time
                return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(data.x), max(data.x)], type='date'),
                                                            yaxis=dict(range=[min(data.y), max(data.y)]))}

            # if we have more than 100 tweets, only load the last 100
            else:
                data = go.Scatter(
                    x=data_frame.unix.values[-100:],                    # x axis is datetime
                    y=data_frame.sentiment_smoothed.values[-100:],      # y axis is sentiment
                    name='Scatter',
                    mode='lines+markers'
                )
                # returns a Plotly Figure, with the data we set earlier and the datetime formatted as calendar time
                return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(data.x), max(data.x)], type='date'),
                                                            yaxis=dict(range=[min(data.y), max(data.y)]))}

    # if there are any errors, write them out to our logfile and identify which callback they were from
    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e) + ": tab 1 graph")
            error_file.write('\n')


# Tab 1 -- display tweets in a scrolling table, color-coded by their sentiment value
@app.callback(Output('tweets-1', 'children'),
              [Input('term-1', 'value'), Input('graph-update-1', 'n_intervals')])
# interval value isn't used in function but is needed so graph updates regularly
def update_tweets(term, interval):
    try:
        # establish connection to the sqlite3 db
        conn = sqlite3.connect(os.path.relpath('database/twitter.db'), check_same_thread=False, timeout=10.0)
        # perform a search on the db based on our given term and load the results into a dataframe
        data_frame = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                                 conn,
                                 params=('%' + term + '%',))

        # this will only execute after the database has been deleted, until there is a tweet about the selected topic
        if data_frame.empty:
            return "There are currently no tweets about this term.  Wait for tweets to appear or select another term"
        # if the dataframe is not empty, update tweets
        else:
            # sort values by time so that we're displaying the same value we're graphing
            data_frame.sort_values('unix', ascending=False, inplace=True)
            # get number of rows
            num_rows = int(len(data_frame))
            # display tweet and sentiment data for the most recent ten tweets
            if num_rows < 10:
                last_ten = data_frame.iloc[:, 1:3]
            else:
                last_ten = data_frame.iloc[:10, 1:3]

            # helper function that returns a color-coded table
            return generate_table_1(last_ten, term, num_rows)

    # if there are any errors, write them out to our logfile and identify which callback they were from
    except Exception as e:
        with open('errors.txt', 'a') as error_file:
            error_file.write(str(e) + ": tab 1 tweets")
            error_file.write('\n')


# Tab 2 -- This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-2', 'options'),
    [Input('active-dropdown-2', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# Tab 2 -- This callback selects the desired candidate from the list the previous callback returns
@app.callback(
    Output('candidate-dropdown-2', 'value'),
    [Input('candidate_dropdown-2', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# Tab 2 -- Updates the graph to show the average daily sentiment score for the selected candidate(s)
@app.callback(Output('line-graph-2', 'figure'),
              [Input('candidate-dropdown-2', 'value')])
def graph_daily_sentiment(candidates):
    try:
        # list to hold the plotly graph objects constructed for each sentiment value
        lines = list()
        # if we have candidates selected, graph their sentiment data
        if candidates:
            # gather data and graph each candidate separately
            for i in candidates:
                # get sentiment data and date for the specified candidate
                query = "SELECT sentiment_date, compound_sentiment_vadersentiment * 100. as score" \
                        + " FROM Candidate_Sentiment" \
                        + " WHERE name = '" \
                        + str(i) \
                        + "';"

                # list to hold the dates each sentiment score was calculated for
                dates = list()
                # list to hold sentiment scores
                score = list()

                # call database using the above candidate and return as a datframe
                sentiment_data = db.select_database(query)

                # iterate through dataframe to retrieve its data, storing dates and sentiment in the appropriate lists
                for index, row in sentiment_data.iterrows():
                    dates.append(row['sentiment_date'])
                    score.append(row['score'])
                # create a Plotly graph object with that sentiment data and add it to the lines list
                lines.append(plotly.graph_objs.Scatter(
                    x=np.asarray(dates),
                    y=np.asarray(score),
                    name=i,
                    mode='lines+markers'
                ))
            # set it as a var so we can return it
            data = lines
            # set up layout (title and axes)
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (0-100%)')
                          )

            # return the data and layout we created above
            return {'data': data, 'layout': layout}
        # if we have no selected candidates, configure an empty graph with the same title and axes, and return it
        else:
            # empty data set
            data = {
                'x': [],
                'y': [],
                'type': 'line'
            }
            # same layout that we defined above
            layout = dict(title='Candidate Sentiment By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Sentiment Score -- (-100% - 100%)'),
                          )
            return {'data': [data], 'layout': layout}

    # if there are any errors, write them out to our logfile and identify which callback they were from
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e) + ": tab 5")
            f.write('\n')


# Tab 3 -- This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-3', 'options'),
    [Input('active-dropdown-3', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# Tab 3 -- This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-3', 'value'),
    [Input('candidate_dropdown-3', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# Tab 3 -- This callback updates a box graph that displays each candidate's twitter metrics
@app.callback(Output('box-graph-3', 'figure'),
              [Input('candidate-dropdown-3', 'value'), Input('metric-dropdown-3', 'value')])
def update_twitter_metrics(candidates, metric):
    # if candidates are selected, graph them
    if candidates:
        # list to hold candidate names
        name_list = list()
        # list to hold twitter values for the selected candidates
        metric_value_list = list()

        # collect data for all candidates
        for name in candidates:
            # select the specified metric values for the specified candidate from the db
            query = "SELECT " + str(metric) + " FROM Twitter_Metrics " + "WHERE [name] = '" + str(name) + "'"
            # run query and store results in a dataframe
            data_table = db.select_database(query)

            # add name to list of names
            name_list.append(name)
            # add metric to list of metrics
            metric_value_list.append(data_table[metric].values[0])

        # add name and metric data to a bar graph data element
        data = go.Bar(
            x=name_list,
            y=metric_value_list,
            name='Bar'
        )

        # create a layout to size x and y based on the max values in the two lists
        layout = go.Layout(xaxis=dict(range=(0 - 1, len(name_list))),
                           yaxis=dict(range=[0, max(metric_value_list)]), )

    # If no candidates are selected, use default data and layout
    else:
        # empty data set
        data = {
            'x': [],
            'y': [],
            'type': 'bar'
        }
        # same layout as above
        layout = {
            'xaxis': {'title': 'Candidates'},
            'yaxis': {'title': metric},
            'barmode': 'relative',
            'title': metric
        }
    # return layout regardless of if we hit the if or the else
    return {'data': [data], 'layout': layout}


# Tab 4 -- This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-4', 'options'),
    [Input('active-dropdown-4', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# Tab 4 -- This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-4', 'value'),
    [Input('candidate_dropdown-4', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# Tab 4 -- This callback sets a title based on the selected options in the three dropdowns
@app.callback(
    Output('title-4', 'children'),
    [Input('candidate-dropdown-4', 'value'),
     Input('policy-dropdown-4', 'value')])
def set_title(selected_candidate, selected_policy):
    # if we have selected a candidate and we want their overview, return accordingly
    if selected_policy == 'Overview' and selected_candidate is not None:
        return "Overview of " + selected_candidate
    # else, return the selected candidate's views on the chosen policy
    elif selected_candidate is not None and selected_policy is not None:
        return selected_candidate + "'s Views On " + selected_policy
    # if no values have been selected yet, return an empty string
    else:
        return ''


# Tab 4 -- This callback displays the main body of text, scraped from wikipedia
@app.callback(
    Output('display-andidate-info-4', 'children'),
    [Input('candidate-dropdown-4', 'value'),
     Input('policy-dropdown-4', 'value')])
def set_display_children(selected_candidate, selected_policy):
    # if no values have been selected yet, return an empty string
    if selected_candidate is None and selected_policy is None:
        return ""

    # append the values for Walsh and Delaney so that their wikipedia searches work correctly
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
    # if there are any errors, write them out to our logfile and identify which callback they were from
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e) + ": tab 4 positions")
            f.write('\n')
    # if that fails, try catch main page
    if candidate_positions is None:
        try:
            candidate_main = wikipedia.page(selected_candidate)
        # if there are any errors, write them out to our logfile and identify which callback they were from
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write(str(e) + ": tab 4 main")
                f.write('\n')
    # if that fails try catch for campaign page
    if candidate_positions is None and candidate_main is None:
        try:
            candidate_campaign = wikipedia.page(selected_candidate + " 2020 presidential campaign")
        # if there are any errors, write them out to our logfile and identify which callback they were from
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write(str(e) + ": tab 4 campaign")
                f.write('\n')

    # lists of possible names for each section - hardcoded based on the formatting of the candidates' wikipedia pages
    agriculture = ["Agriculture", "Agriculture and rural issues"]
    campaign_finance = ["Campaign finance reform", "Campaign finance"]
    childcare = ["Child care", "Family policy"]
    criminal_justice_reform = ["Criminal justice reform", "Criminal justice"]
    drugs = ["Drug Policy", "Drug policy reform", "Drug laws", "Drug policy", "War on Drugs", "Drugs"]
    education = ["Education", "Higher education", "Education policy"]
    environment = ["Environment", "Environmentalism", "Climate change and environment", "Climate change",
                   "Environmental policy", "Environment and energy", "Energy and environment"]
    foreign_policy = ["Foreign policy", "Foreign policy and national security", "Diplomacy", "Foreign affairs",
                      "Foreign policy and defense"]
    gov_shutdown = ["Government shutdown", "2018–19 government shutdown"]
    gun_laws = ["Gun laws", "Gun rights", "Gun control", "Gun Policy", "Guns", "Gun regulation", "Gun law",
                "Gun policy"]
    healthcare = ["Health care", "Healthcare", "Health insurance", "Health care policy"]
    housing = ["Housing"]
    immigration = ["Immigration", "Immigration policy", "Immigration and border security",
                   "Immigration on southern border"]
    lgbt_rights = ["LGBTQ+ rights", "LGBT rights", "LGBT issues", "LGBTQ community", "LGBTQ rights", "LGBTQ issues"]
    minimum_wage = ["Minimum wage"]
    marijuana = ["Cannabis legalization", "Cannabis", "Medical marijuana", "Marijuana"]
    net_neutrality = ["Net neutrality", "Net Neutrality"]
    opioids = ["Opioids", "Opioid epidemic"]
    other = ["Freedom Dividend (UBI)", "Stop-and-frisk"]
    trade = ["Trade", "Trade policy"]
    veterans = ["Veterans Issues", "Veterans"]
    womens_issues_abortion = ["Women's issues and abortion", "Abortion", "Women's rights"]

    # only enter this loop and begin selection if we've actually selected a candidate
    if selected_candidate is not None:
        # return their summary if we select overview
        if selected_policy == 'Overview':
            return wikipedia.summary(selected_candidate, auto_suggest=False)
        # else, return the selected policy from one of their wikipedia pages
        else:
            # if no policy, return an empty string
            if selected_policy is None:
                return ''
            elif selected_policy == "Agriculture":
                return find_policy(agriculture, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Campaign Finance":
                return find_policy(campaign_finance, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Childcare":
                return find_policy(childcare, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Criminal Justice Reform":
                return find_policy(criminal_justice_reform, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Drugs":
                return find_policy(drugs, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Education":
                return find_policy(education, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Environment":
                return find_policy(environment, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Foreign Policy":
                return find_policy(foreign_policy, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Government Shutdown":
                return find_policy(gov_shutdown, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Gun Laws":
                return find_policy(gun_laws, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Healthcare":
                return find_policy(healthcare, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Housing":
                return find_policy(housing, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Immigration":
                return find_policy(immigration, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "LGBT Rights":
                return find_policy(lgbt_rights, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Minimum Wage":
                return find_policy(minimum_wage, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Marijuana":
                return find_policy(marijuana, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Net Neutrality":
                return find_policy(net_neutrality, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Opioids":
                return find_policy(opioids, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Other":
                return find_policy(other, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Trade":
                return find_policy(trade, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Veterans":
                return find_policy(veterans, candidate_positions, candidate_main, candidate_campaign)
            elif selected_policy == "Women's Issues/Abortion":
                return find_policy(womens_issues_abortion, candidate_positions, candidate_main, candidate_campaign)
            # if we can't find the policy, return a string saying so
            else:
                return "There are no wikipedia entries available for this policy"


# Tab 5 -- graph web-scraped poll data
@app.callback(Output('line-graph-5', 'figure'),
              [Input('candidate-dropdown-5', 'value')])
def graph_polls(candidates):
    try:
        # list to hold the plotly graph objects constructed for each sentiment value
        lines = list()

        # if we have candidates selected, graph their sentiment data
        if candidates:
            # initialize query here in case both candidate calls fail
            query = ''
            # do this whole process for each candidate
            for candidate in candidates:
                # queries are identical except one gets biden's percentage and one get's bernie's
                if candidate == 'Joe Biden':
                    query = "SELECT pollster, poll_dates, sample_size, biden_pct as pct, spread " \
                            "FROM Polls2;"
                elif candidate == 'Bernie Sanders':
                    query = "SELECT pollster, poll_dates, sample_size, bernie_pct as pct, spread " \
                            "FROM Polls2;"
                # list to hold dates polls were conducted on
                dates = list()
                # list to hold polling values
                percent = list()
                # list to hold other poll data (pollster, sample size, spread) to use as hover text
                hover = list()
                # query db and return as dataframe
                candidate_info = dberic.select_database(query)

                # sort by date and take the mean of like dates
                candidate_info = candidate_info.sort_values(by='poll_dates')
                # grouping and taking the mean allows us to only have one data point per candidate per day
                candidate_info_abridged = candidate_info.groupby(by='poll_dates', as_index=False).mean()

                # loop through and create lists
                for index, row in candidate_info_abridged.iterrows():
                    # append date to dates list for each row
                    dates.append(row['poll_dates'])
                    # append percentages to percent list for each row
                    percent.append(row['pct'])
                    # create hovertext
                    hovertext = ""
                    # loop through original array - if any date values match, add their metadata to the hovertext
                    for index2, row2 in candidate_info.iterrows():
                        if row2['poll_dates'] == row["poll_dates"]:
                            hovertext += "Pollster: " + row2['pollster'] + ", Sample Size: " + row2['sample_size'] + \
                                         ", Spread: " + row2['spread'] + "<br>"
                    # add completed hovertext strings to the list
                    hover.append(hovertext)

                # add a graph object with appropriate position and hovertext for each row
                lines.append(plotly.graph_objs.Scatter(
                    x=np.asarray(dates),
                    y=np.asarray(percent),
                    name=candidate,
                    hovertext=np.asarray(hover),
                    mode='lines+markers'
                ))
            # set to data for readability
            data = lines
            # set layout with title and x/y axis labels
            layout = dict(title='Polling Data By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Percent'),
                          )
            # return our data and our layout
            return {'data': data, 'layout': layout}

        # if no candidates, return default layout
        else:
            # empty data set
            data = {
                'x': [],
                'y': [],
                'type': 'line'
            }
            # same layout as above
            layout = dict(title='Polling Data By Date',
                          xaxis=dict(title='Date'),
                          yaxis=dict(title='Percent'),
                          )
            return {'data': [data], 'layout': layout}

    # if there are any errors, write them out to our logfile and identify which callback they were from
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e) + ": tab 2")
            f.write('\n')


# Tab 6 -- This callback sets whether the second dropdown filters for active candidates or not
@app.callback(
    Output('candidate-dropdown-6', 'options'),
    [Input('active-dropdown-6', 'value')])
def set_candidate_options(active_or_not):
    return [{'label': i, 'value': i} for i in all_options[active_or_not]]


# Tab 6 -- This callback selects the desired candidate
@app.callback(
    Output('candidate-dropdown-6', 'value'),
    [Input('candidate_dropdown-6', 'options')])
def set_candidate_value(available_options):
    return available_options[0]['value']


# Tab 6 -- display tweets from the selected candidate about the selected policy
@app.callback(
    Output('tweets-list-6', 'children'),
    [Input('candidate-dropdown-6', 'value'),
     Input('input-6', 'value')])
def tweets_about_policy(selected_candidate, policy_input):
    # only display if we have actually selected a candidate
    if selected_candidate is not None:

        # query database for the relevant tweets about the selected policy by the selected candidate
        relevant_tweets = db.select_database("SELECT text, favorite_count, retweet_count FROM "
                                             "Candidate_Tweets "
                                             "WHERE text LIKE '%" + policy_input + "%' "
                                             "AND user_name = '" + selected_candidate + "'")

        # use iloc here to reverse the table so it shows most recent first
        relevant_tweets = relevant_tweets.iloc[::-1]

        # return an html table containing the desired tweets
        return generate_table_6(relevant_tweets, len(relevant_tweets.index))

    # if no candidate selected, return a blank string
    else:
        return ""


# Tab 6 -- display the number of tweets from the selected candidate about the selected policy
@app.callback(
    Output('num-tweets-6', 'children'),
    [Input('candidate-dropdown-6', 'value'),
     Input('input-6', 'value')])
def num_tweets_about_policy(selected_candidate, policy_input):
    # only display if we have actually selected a candidate
    if selected_candidate is not None:

        # query database for the relevant tweets about the selected policy by the selected candidate
        num_tweets = db.select_database("SELECT tweet_id FROM "
                                        "Candidate_Tweets "
                                        "WHERE text LIKE '%" + policy_input + "%' "
                                        "AND user_name = '" + selected_candidate + "'")

        # return string containing the number of relevant tweets
        return selected_candidate + " has " + str(len(num_tweets.index)) + " tweets about " + policy_input + "."

    # if no candidate selected, return a blank string
    else:
        return ""


# Tab 6 -- display the average sentiment of tweets from the selected candidate about the selected policy
@app.callback(
    Output('sentiment-6', 'children'),
    [Input('candidate-dropdown-6', 'value'),
     Input('input-6', 'value')])
def sentiment_tweets_about_policy(selected_candidate, policy_input):
    # only display if we have actually selected a candidate
    if selected_candidate is not None:

        # query database for the relevant tweets about the selected policy by the selected candidate
        relevant_tweets = db.select_database("SELECT text FROM "
                                             "Candidate_Tweets "
                                             "WHERE text LIKE '%" + policy_input + "%' "
                                             "AND user_name = '" + selected_candidate + "'")

        # create a new sentiment analyzer and initialize the relevant var
        analyzer = SentimentIntensityAnalyzer()
        sentiment_total = 0

        # for each tweet, analyze sentiment and add its score to the total
        for index, row in relevant_tweets.iterrows():
            vs = analyzer.polarity_scores(row['text'])
            sentiment = vs['compound']
            sentiment_total += sentiment

        # try catch is here in case there are 0 tweets in the dataframe
        try:
            # divide sentiment by total # of tweets to get the average
            avg_sentiment = sentiment_total/len(relevant_tweets.index)
        except ZeroDivisionError:
            # if no tweets, average sentiment is naturally zero
            avg_sentiment = 0

        # return sentiment score
        return "Those tweets have an average sentiment score of " + str(avg_sentiment) + "."

    # if no candidate selected, return a blank string
    else:
        return ""


# helper functions stored down here

# Tab 1 -- dynamically color a cell in our table based
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


# Tab 1 -- generates a styled table for use in updating the scrolling table of tweets
def generate_table_1(data_frame, term, num_rows):
    # array to hold the table rows
    rows = []

    # loop through dataframe - it will have 10 or less rows so we specify that here
    for i in range(min(num_rows, 10)):
        # array to hold our current table row
        row = []
        for col in data_frame.columns:
            # get sentiment value
            sentiment = data_frame.iloc[i][1]
            # get cell color based on sentiment
            style = cell_style(sentiment)
            # add the row to the row array with our pre-determined color
            row.append(html.Td(data_frame.iloc[i][col], style=style))
        # add the row to the table array
        rows.append(html.Tr(row))

    # construct the table
    return html.Table(
        # construct header
        [html.Tr([html.Th("Live twitter feed for the term \"" + term + "\"", style={'font-size': 'x-large'})])]
        # add table body
        + rows)


# Tab 6 -- generates a table to display the selected tweets
def generate_table_6(data_frame, num_rows):
    # array to hold the table rows
    rows = []

    # loop through dataframe
    for i in range(num_rows):
        # array to hold our current table row
        row = []
        for col in data_frame.columns:
            # add the row to the row array
            row.append(html.Td(data_frame.iloc[i][col]))
        # add the row to the table array
        rows.append(html.Tr(row))

    # construct the table
    return html.Table(
        # construct header
        [html.Tr([html.Th("Tweets"), html.Th("Favorites"), html.Th("Retweets")], style={'font-size': 'large'})]
        # add table body
        + rows)


# Tab 4 -- find the specified policy on one of the candidate's wikipedia pages
def find_policy(policy_name, candidate_positions, candidate_main, candidate_campaign):
    # check the "political positions of" page first, if it exists (it will usually be the most complete of the three)
    if candidate_positions is not None:
        # loop through our hardcoded list of options
        for option in policy_name:
            # if we don't find it, continue
            if candidate_positions.section(option) is None:
                continue
            # if found, return
            else:
                return candidate_positions.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic and we return accordingly
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy

    # next check their main page
    elif candidate_main is not None:
        # loop through our hardcoded list of options
        for option in policy_name:
            # if we don't find it, continue
            if candidate_main.section(option) is None:
                continue
            # if found, return
            else:
                return candidate_main.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic and we return accordingly
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy

    # if that fails, check their campaign page (only necessary for weld and yang)
    elif candidate_campaign is not None:
        # loop through our hardcoded list of options
        for option in policy_name:
            # if we don't find it, continue
            if candidate_campaign.section(option) is None:
                continue
            # if found, return
            else:
                return candidate_campaign.section(option)
        # if the for loop finishes, then the candidate has no policy on the topic and we return accordingly
        no_policy = "This candidate does not have an entry on Wikipedia for this policy."
        return no_policy

    # if the policy does not exist on any of the three pages, log the error and return an "error" string
    else:
        with open('errors.txt', 'a') as f:
            f.write("policy not found: " + policy_name)
            f.write('\n')
        no_candidate = "This candidate does not have an entry on Wikipedia."
        return no_candidate


# main program
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='80')
