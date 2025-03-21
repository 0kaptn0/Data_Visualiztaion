import pandas as pd
import dash
from dash import html , dcc
from dash.dependencies import Input,Output,State
import plotly.express as px
import plotly.graph_objects as go 
from dash import no_update
import datetime as dt 

#creating dpp
app=dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
#reading the data
df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')
#extracting month and year from date column
df['Year']=pd.to_datetime(df['Date']).dt.year
df['month']=pd.to_datetime(df['Date']).dt.month_name()
#app layout 
app.layout=html.Div(children=[html.H1('Australia Wildfire Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
html.Div([
    html.Div([
        html.H2('Select Region:', style={'margin-right': '2em'}),
        dcc.RadioItems(['NSW','QL','SA','TA','VI','WA'],'NSW',id='region',inline=True)

    ]),
    html.Div([
        html.H2('select year:',style={'margin-right':'2em'}),
        dcc.Dropdown(df.Year.unique(),value=2005,id='year')

    ]),
    html.Div([
    html.Div(dcc.Graph(),id='figure'),
    html.Div(dcc.Graph(),id='figure2')],style={'display':'flex'}),

])
])
#app layout ends

#adding callback function
@app.callback(
   [Output('figure','children'),
    Output('figure2','children')],
   [Input('region','value'),
    Input('year','value')]
)
#adding the callback function
def regn_year(input_region,input_year):
    region_data=df[df['Region']==input_region]
    year_data=region_data[region_data['Year']==input_year]
    #figure one monthly avg estimate fire area
    est_data=year_data.groupby('month')['Estimated_fire_area'].mean().reset_index()
    fig1=px.pie(est_data,values='Estimated_fire_area',names='month',title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))
    #figure two-monthly avg count of pixels for presumed vegetation fires
    veg_data=year_data.groupby('month')['Count'].mean().reset_index()
    fig2=px.bar(veg_data,x='month',y='Count',title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))
    
    return[dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)]



#run the app
if __name__ =='__main__':
    app.run_server()
