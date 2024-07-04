import pandas as pd
from dash import Dash, callback, Input, Output, html, dcc
from mitosheet.mito_dash.v1 import Spreadsheet, mito_callback, activate_mito
from typing import List
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template



load_figure_template("pulse")
app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE, dbc.icons.BOOTSTRAP])
activate_mito(app)

CSV_URL = pd.read_csv('cleaned_superstore.csv', index_col=False)
CSV_URL = CSV_URL[['order_date', 'category', 'sales']]

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(Spreadsheet(CSV_URL, id={'type': 'spreadsheet', 'id': 'sheet'}), width=8),
        dbc.Col([dcc.Dropdown(id='dropdown', value='category', placeholder="Select a dimension", className='mb-2'), dcc.Graph(id='output-graph', config={'displayModeBar': False})], width=4)]),
    dbc.Row([html.Div(id='output')]),
],

    fluid=True,)


@mito_callback(
    Output('output-graph', 'figure'),
    Output('dropdown', 'options'),
    Output('output', 'children'),
    Input({'type': 'spreadsheet', 'id': 'sheet'}, 'spreadsheet_result'),
    Input('dropdown', 'value')
)
def update_code(spreadsheet_result, dopdown_input):
    # capture current dataframe from mito object
    dfs: List[pd.DataFrame] = spreadsheet_result.dfs()
    df = dfs[0]
    fig = px.histogram(df, x=dopdown_input, y='sales', text_auto='0.2s', title=f'sales by {dopdown_input}')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), yaxis=dict(showticklabels=False))
    dropdown_options = df.columns.tolist()

    # Remove 'sales' element
    if 'sales' in dropdown_options:
        dropdown_options.remove('sales')
    return fig, dropdown_options, html.Div([
        html.Code(spreadsheet_result.code())
    ])

if __name__ == '__main__':
    app.run_server(debug=True)