# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

for i,u in spacex_df['Booster Version'].iteritems():
    if u.startswith('F9 v1.0'):
        spacex_df.at[i,'Booster Version Kategory'] = 'F9 v1.0'
    if u.startswith('F9 v1.1'):
        spacex_df.at[i,'Booster Version Kategory'] = 'F9 v1.1'
    if u.startswith('F9 FT'):
        spacex_df.at[i,'Booster Version Kategory'] = 'F9 FT'
    if u.startswith('F9 B4'):
        spacex_df.at[i,'Booster Version Kategory'] = 'F9 B4'
    if u.startswith('F9 B5'):
        spacex_df.at[i,'Booster Version Kategory'] = 'F9 B5'

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label':'All Sites', 'value':'ALL'},
                                        {'label':'CCAFS LC-40', 'value':'site1'},
                                        {'label':'CCAFS SLC-40', 'value':'site2'},
                                        {'label':'KSC LC-39A', 'value':'site3'},
                                        {'label':'VAFB SLC-4E', 'value':'site4'}
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                marks={0:'0',100:'100'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
              Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def get_charts(entered_site, slider_range):
    filtered_df = spacex_df
    low, high = slider_range

    if entered_site == 'ALL':
        fig = px.pie(filtered_df,
            values='class',
            names='Launch Site', 
            title='Total success launches by site')

        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig_2 = px.scatter(filtered_df[mask],
            x='Payload Mass (kg)',
            y='class', 
            color='Booster Version Kategory',
            title='Correlation between payload and success for all sites')

    else:
        # return the outcomes piechart for a selected site
        if entered_site == 'site1':
            filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
            mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
            title_site = 'Total success launches for site CCAFS LC-40'
            title_site_2 = 'Correlation between payload and success for site CCAFS LC-40'
            
        if entered_site == 'site2':
            filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
            title_site = 'Total success launches for site CCAFS SLC-40'
            title_site_2 = 'Correlation between payload and success for site CCAFS SLC-40'

        if entered_site == 'site3':
            filtered_df = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
            mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
            title_site = 'Total success launches for site KSC LC-39A'
            title_site_2 = 'Correlation between payload and success for site KSC LC-39A'

        if entered_site == 'site4':
            filtered_df = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
            mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
            title_site = 'Total success launches for site VAFB SLC-4E'
            title_site_2 = 'Correlation between payload and success for site VAFB SLC-4E'

        fig = px.pie(filtered_df, 
            names='class', 
            title=title_site)
        
        fig_2 = px.scatter(filtered_df[mask], 
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Kategory',
            title=title_site_2)

    return fig, fig_2

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Run the app
if __name__ == '__main__':
    app.run_server()
