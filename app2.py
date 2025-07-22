import pandas as pd
import plotly.express as px
import json
from dash import Dash, dcc, html, Input, Output

# Load data
json1 = "C:/Users/Dhruv/OneDrive/Desktop/Summer training/statesofindia.geojson"
csv_path = "C:/Users/Dhruv/OneDrive/Desktop/Summer training/india-districts-census-2011.csv"

df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()  # Clean column names

with open(json1, "r") as f:
    geojson_data = json.load(f)

# Initialize Dash app
app = Dash(__name__)
app.title = "India Population Dashboard"

states = sorted(df['State name'].unique())

# App layout
app.layout = html.Div([
    html.H1("Population Map of India", style={'textAlign': 'center'}),

    html.Label("Select a State"),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in states],
        value=states[0]
    ),

    html.Label("Select a District"),
    dcc.Dropdown(id='district-dropdown'),

    html.Br(),

    dcc.Graph(id='choropleth-map'),

    html.Div(id='population-display', style={'fontSize': 24, 'textAlign': 'center'})
])


# Callback to update districts based on selected state
@app.callback(
    Output('district-dropdown', 'options'),
    Output('district-dropdown', 'value'),
    Input('state-dropdown', 'value')
)
def update_district_dropdown(selected_state):
    filtered = df[df['State name'] == selected_state]
    districts = sorted(filtered['District name'].unique())
    return [{'label': d, 'value': d} for d in districts], districts[0]


# Callback to update map and population display
@app.callback(
    Output('choropleth-map', 'figure'),
    Output('population-display', 'children'),
    Input('state-dropdown', 'value'),
    Input('district-dropdown', 'value')
)
def update_map_and_population(selected_state, selected_district):
    state_df = df[df['State name'] == selected_state]

    # Choropleth map
    fig = px.choropleth(
    df,  # Use full dataframe
    geojson=geojson_data,
    featureidkey="properties.ST_NM",
    locations="State name",
    color="Population",
    color_continuous_scale="Viridis",
    title="Population by State"
)
    fig.update_geos(fitbounds="locations", visible=False)



    # District population display
    district_pop = state_df[state_df['District name'] == selected_district]['Population'].values[0]
    pop_text = f"Population of {selected_district}: {district_pop:,}"

    return fig, pop_text


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True, port=8051)
