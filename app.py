import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_table import DataTable
from dash.dependencies import Output, Input, State
from model import scraper, r
import pandas as pd
from pandas import DataFrame
import urllib.parse


app = dash.Dash(__name__,external_stylesheets = [dbc.themes.FLATLY])

cities = pd.read_csv("complete_city_list.csv", header = None)
cities['value'] = cities.iloc[:,0]
cities.columns = ['label','value']
base =['Page No.', 'url', 'organization', 'title', 'experience', 'skill','description', 'salary', 'postedby', 'time']

navbar = dbc.NavbarSimple(
        brand="Naukri Scraper",
        brand_href="#",
        sticky='top',    
        dark = True,
        color = 'primary',
        fluid = True
    )


body = dbc.Container(
    [
        dcc.Interval(
            id="interval",
            interval=1*500, # in milliseconds
            n_intervals=0
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "cities",
                            options = cities.to_dict('records'),
                            value = None,
                            multi = True,
                            placeholder = "Select Cities"
                        ),
                    ], 
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id = "freshness",
                            options = [
                                {'label': "Last 1 Day",'value': 1}, 
                                {'label': "Last 3 Days",'value': 3},
                                {'label': "Last 7 Days",'value': 7},
                                {'label': "Last 15 Days",'value': 15},
                                {'label': "Last 30 Days",'value': 30}, 
                                {'label': "All",'value': 0}],
                            value = None,
                            placeholder = "Select Freshness"
                        ),
                    ], 
                ),
                # dbc.Col(
                #     [
                #         dcc.Input(
                #             id = "page_limit",
                #             type = "number",
                #             value = 10,
                #             placeholder = "Select a Page Limit"
                #         ),
                #     ],
                # ),                
                dbc.Col(
                    [
                        dbc.Button("Lets Go!", id = "letsgo",color = "primary")
                    ], 
                )
            ], className = "mt-3"
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Please Select a City (or List of Cities) and Freshness", style = {'margin': '0px'})
                    ], id = "title", width = 8
                ),
                dbc.Col(
                    [
                        dbc.Button(id = "page-number", color = "success")
                    ], width = "auto",
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            children = [
                                html.A("Download Scraped Data as CSV", id = "download", download="rawdata.csv", href = "", target="_blank", style = {'color': '#fff'})
                            ],
                            color = "primary")
                    ], width = "auto" 
                )
            ], className = "mt-3", justify = "between",
        ),

        dbc.Row(
            [
                dcc.Loading(id = "loading",
                    children = [
                        dbc.Col(
                            [
                                DataTable(
                                    id='table',
                                    columns = [{'name': i, 'id': i} for i in base],
                                    data=[],
                                    style_cell={
                                        'padding': '5px',
                                        'width': '189px',
                                        'overflow': 'hidden',
                                        'maxWidth': '189px',
                                        'textAlign': 'center'
                                    },
                                    style_header={
                                        'fontWeight': 'bold',
                                        'textAlign': 'center'
                                    },
                                    style_cell_conditional=[{
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }],
                                    pagination_mode="fe",
                                    pagination_settings={
                                        "current_page": 0,
                                        "page_size": 20,
                                    },
                                    style_table={
                                        'maxWidth': '100%',
                                    },
                                ),
                            ], width = 12
                        )
                    ]
                )
            ], className = "mt-2"
        )
        
    ], fluid = True
)


app.layout = html.Div([navbar,body])


@app.callback(
    Output("title","children"),
    [Input("letsgo","n_clicks")],
    [State("cities","value"),
    State("freshness","value")]
)
def update_title(clicks,cities,freshness):
    if clicks is None:
        raise dash.exceptions.PreventUpdate
    if clicks > 0:
        new_cities = ", ".join(cities)
        if freshness == 0:
            freshness = "All"
        return html.H3(f"Jobs Released in {new_cities} over the last {freshness} days", style = {'margin': '0px'})    

@app.callback(
    Output("table","data"),
    [Input("letsgo","n_clicks")],
    [State("cities","value"),
    State("freshness","value")]    
)
def update_table(clicks,cities,freshness):
    if clicks is None or freshness is None or cities is None:
        return []
    if clicks > 0:
        data, time_scraped = scraper(cities = cities, freshness = freshness)
        return data.to_dict('records')

@app.callback(
    Output('download', 'href'),
    [Input('table', 'data')]
)
def download_df(data):
    if data == []:
        return ""    
    dff = DataFrame(data)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

@app.callback(
    [Output("page-number","children"),
    Output("page-number","color")],
    [Input("interval","n_intervals")]
)
def update_page(interval):
    page = r.get("page")
    if page is None:
        return ["Awaiting Scraping Instructions","warning"]
    try:
        return [f"Scraping page {int(page)}...","warning"]
    except:
        return [page.decode("utf-8"), "success"]

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host = '192.168.1.73', 
        port = 8050
    ) 