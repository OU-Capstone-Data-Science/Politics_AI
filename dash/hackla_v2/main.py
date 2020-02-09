import dash
import numpy
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import tab_1, tab_2, tab_3, tab_4, tab_5
import sqlite3
import plotly.graph_objs as go
import pandas as pd
import plotly
from IPython.core.display import display

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H1('Boys Rule'),
dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
        dcc.Tab(label='Tab Three', value='tab-3-example'),
        dcc.Tab(label='Tab Four', value='tab-4-example'),
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
        conn = sqlite3.connect('C:\\Users\\Alex\\PycharmProjects\\Politics_AI\\jacob_duvall\\twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn,
                         params=('%' + term + '%',))
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)

        X = df.unix.values[-100:]
        Y = df.sentiment_smoothed.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]),)}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

@app.callback(Output('tweets', 'children'),
              [Input('term', 'value'), Input('graph-update', 'n_intervals')])
def update_tweets(term, ignore):
    try:
        conn = sqlite3.connect('C:\\Users\\Alex\\PycharmProjects\\Politics_AI\\jacob_duvall\\twitter.db')
        c = conn.cursor()
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn,
                     params=('%' + term + '%',))
        df.sort_values('unix', inplace=True)
        lastten = df.iloc[-10:, 1:3]

        def generate_table(dataframe, max_rows=10):
            return html.Table(
                # Header
                [html.Tr([html.Th("Live twitter feed for the term \"" + term + "\"")])] +

                # Body
                for col in dataframe.columns:
                    if(lastten.iloc[i, 1:2] )
                [html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))]
            )
        #lastten = df.tweet.values[-10:]
        #lastten_list = list(lastten)
        #table_html = ""
        #for tweet in lastten_list:
        #    table_html += "\n<tr>\n<td>" + tweet + "</td>\n</tr>"
        #return table_html
        return generate_table(lastten)

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')

# Tab 2 callback -- ERIC
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

# Tab 3 callback -- JACOB
@app.callback(Output('page-3-content', 'children'),
              [Input('page-3-radios', 'value')])
def page_3_radios(value):
    return 'You have selected "{}"'.format(value)

# Tab 4 callback
@app.callback(Output('page-4-content', 'children'),
              [Input('page-4-radios', 'value')])
def page_4_radios(value):
    return 'You have selected "{}"'.format(value)

# Tab 5 callback
@app.callback(Output('page-5-content', 'children'),
              [Input('page-5-radios', 'value')])
def page_5_radios(value):
    return 'You have selected "{}"'.format(value)



app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)