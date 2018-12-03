
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
df = pd.read_csv('nama_10_gdp_1_Data.csv')

df= df.drop(df[df.Value.isin([':'])].index) 
df_cleaned = df[~df.GEO.str.contains("Euro")]

available_indicators = df_cleaned['NA_ITEM'].unique()
avaliable_units = df_cleaned['UNIT'].unique()
avaliable_countries = df_cleaned['GEO'].unique()

app.layout = html.Div([
    html.H1('Thomas Deciderus Final Project', style={'textAlign': 'center', 'color': 'blue'}),
    html.H2('Indicators Figures',style={'textAlign': 'center', 'color': 'black'}),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            html.Div(style={'height': 15}),
            dcc.RadioItems(
                id='Units',
                options=[{'label': i, 'value': i} for i in avaliable_units],
                value='Chain linked volumes, index 2010=100')
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            html.Div(style={'height': 15}),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df_cleaned['TIME'].min(),
        max=df_cleaned['TIME'].max(),
        value=df_cleaned['TIME'].max(),
        step=None,
        marks={str(TIME): str(TIME) for TIME in df_cleaned['TIME'].unique()}
    ),
    html.Div(style={'height': 80}),
    
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='countries2',
                options=[{'label': i, 'value': i} for i in avaliable_countries],
                value='Belgium'
            ),
        html.Div(style={'height': 15}),
        dcc.Dropdown(
                id='UNITS2',
                options=[{'label': i, 'value': i} for i in avaliable_units],
                value='Chain linked volumes, index 2010=100')
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis_column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value="Gross domestic product at market prices"
            ),
            html.Div(style={'height': 15}),
            dcc.RadioItems(
                id='yaxis_type2',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%','float':'right' ,'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic2')])
    
    
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('Units', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name,
                yaxis_type, TIME_value, Units):
    dff = df_cleaned[df_cleaned['TIME'] == TIME_value]
    dfu = dff[dff['UNIT'] == Units]
    
    return {
        'data': [go.Scatter(
            x=dfu[dfu['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dfu[dfu['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dfu[dfu['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if Units == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 50, 't': 50, 'r': 90},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('countries2', 'value'),
     dash.dependencies.Input('yaxis_column2', 'value'),
     dash.dependencies.Input('yaxis_type2', 'value'),
     dash.dependencies.Input('UNITS2', 'value')])
    
def update_graph2(countries2, yaxis_column2,yaxis_type2, UNITS2):
    
    dff = df_cleaned[(df_cleaned['GEO'] == countries2)& (df_cleaned['UNIT'] == UNITS2)]

    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(), #Needs to get all the unique values of TIME
            y=dff[dff['NA_ITEM'] == yaxis_column2]['Value'],
            mode='lines'
        )],
        
        'layout': go.Layout(
            xaxis={
                'title': 'years'
            },
            yaxis={
                'title': yaxis_column2,
                'type': 'linear' if yaxis_type2 == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 50, 't': 50, 'r': 90},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()

