# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# mark the range over which the payload mass would slide
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX launch records dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 60}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = [
                                        {'label':'All sites', 'value':'ALL'},
                                        # the label and value are the respective launch site names in spacex_df
                                        # launch site 1: 'CCAFS LC-40'
                                        {'label': spacex_df['Launch Site'].unique()[0], 
                                         'value': spacex_df['Launch Site'].unique()[0]},
                                         # launch site 2: 'VAFB SLC-4E'
                                        {'label': spacex_df['Launch Site'].unique()[1],
                                         'value': spacex_df['Launch Site'].unique()[1]},
                                         # launch site 3: 'KSC LC-39A'
                                        {'label': spacex_df['Launch Site'].unique()[2],
                                         'value': spacex_df['Launch Site'].unique()[2]},
                                         # launch site 4: 'CCAFS SLC-40'
                                        {'label': spacex_df['Launch Site'].unique()[3],
                                         'value': spacex_df['Launch Site'].unique()[3]},
                                    ],
                                    value = 'ALL',
                                    placeholder = 'Select a launch site here.',
                                    searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id = 'success-pie-chart')),
                                html.Br(),
                         
                                # TASK 3: Add a range slider to select payload
                                html.P("Payload range (kg):"),
                                
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id = 'payload-slider',
                                    # define the range over which the payload mass would slide
                                    min = 0,
                                    max = 10000,
                                    marks = {'0': 0, '2000': 2000, '4000': 4000, '6000': 6000, 
                                             '8000': 8000, '10000': 10000},
                                    value = [min_payload, max_payload],
                                    step=1000
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
                                ])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output.
# pie chart callback
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
# pie chart function for launch success rates all sites and respective sites 
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,
                     values='class',
                     names='Launch Site',
                     title='Total successfull launches by site')
        return fig
    else:
        fig = px.pie(filtered_df,
                     names='class',
                     title=f'Launch success for {entered_site}.')
    return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(  
    Output(component_id='success-payload-scatter-chart', component_property='figure'),  
    [Input(component_id='site-dropdown', component_property='value'),  
    Input(component_id='payload-slider', component_property='value')]  
)  
def update_scatter_chart(entered_site, payload_range):  
    # Filter by launch site  
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site] if entered_site != 'ALL' else spacex_df  
    
    # Filter by payload range  
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &   
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]  
    
    # Create scatter plot  
    fig = px.scatter(data_frame=filtered_df,  
                     y='class',  
                     x='Payload Mass (kg)',  
                     color='Booster Version Category',  
                     title=f'Launch success for {entered_site} according to payload and booster version.',  
                     labels={'class': 'Launch outcome'})  
    return fig

# Run the app  
if __name__ == '__main__':  
    app.run_server(host='localhost', port=8050)
