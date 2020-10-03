import os
from datetime import date
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.graph_objs as go

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

basedir = os.path.abspath(os.path.dirname(__file__))
data_json = basedir+'/amazing-insight.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(data_json, scope)
connection = gspread.authorize(creds)

worksheet = connection.open("Surfactant_Database").sheet1
dv = get_as_dataframe(worksheet)
dv = dv.loc[:, ~dv.columns.str.contains('^Unnamed')]

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[
                    {
                        'name' : 'image',
                        'property' : 'og:image',
                        'content' : 'assets/thumbnail.PNG'
                    }
])
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Foam Database"

if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-3dscatterplot'

today = date.today()
today = today.strftime("%m/%d/%Y")

dv.dropna(
    axis=0,
    how='all',
    thresh=None,
    subset=None,
    inplace=True
)

dv.fillna("None", inplace=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content'),
])

home = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([html.H1("Foam Database")],
                style={'text-align':"center", "margin-right":"auto","margin-left":"auto", 'color':"white","width": "80%","padding-top":"10%"}),

            html.Div([
                html.Div(dcc.Dropdown(id="select-xaxis", placeholder = "Select x-axis", value = "Temperature (C)",
                    options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                ),
                html.Div(dcc.Dropdown(id="select-yaxis", placeholder = "Select y-axis", value = "Pressure (Psi)",
                    options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False)
                ),
                html.Div(dcc.Dropdown(id="select-zaxis", placeholder = "Select z-axis", value = "Halflife (Min)",
                    options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False)
                )
            ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto", "width": "80%"}),

            html.Div([
                dbc.Row([
                    dcc.RadioItems(
                        id='toggle',
                        options=[{'label': i, 'value': i} for i in ['Show Less','Show More']],
                        value='Show Less',
                        labelStyle={"padding-right":"10px","margin":"auto"},
                        style={"text-align":"center","margin":"auto"}
                    ),
                ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto"}),

                html.Div(id='controls-container', children=[
                    
                    html.Hr(),
                    
                    html.Details([
                        html.Summary("Gasses"),
                        dcc.Checklist(
                            id = 'gasses',
                            options= [{'label': gas, 'value': gas} for gas in list(dict.fromkeys(dv['Gas']))],
                            value = list(dict.fromkeys(dv['Gas'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Surfactants"),
                        dcc.Checklist(
                            id = 'surfactants',
                            options= [{'label': surfactant, 'value': surfactant} for surfactant in list(dict.fromkeys(dv['Surfactant']))],
                            value = list(dict.fromkeys(dv['Surfactant'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Surfactant Concentrations"),
                        dcc.Checklist(
                            id = 'sconc',
                            options= [{'label': sc, 'value': sc} for sc in list(dict.fromkeys(dv['Surfactant Concentration']))],
                            value = list(dict.fromkeys(dv['Surfactant Concentration'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Additives"),
                        dcc.Checklist(
                            id = 'additives',
                            options= [{'label': ad, 'value': ad} for ad in list(dict.fromkeys(dv['Additive']))],
                            value = list(dict.fromkeys(dv['Additive'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Additive Concentrations"),
                        dcc.Checklist(
                            id = 'aconc',
                            options= [{'label': adc, 'value': adc} for adc in list(dict.fromkeys(dv['Additive Concentration']))],
                            value = list(dict.fromkeys(dv['Additive Concentration'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Liquid Phase"),
                        dcc.Checklist(
                            id = 'lp',
                            options= [{'label': li, 'value': li} for li in list(dict.fromkeys(dv['LiquidPhase']))],
                            value = list(dict.fromkeys(dv['LiquidPhase'])),
                            labelStyle={'display': 'block'}
                        ),
                    ]),
                    
                    html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3}),

            dcc.Link('About', href='/about',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18}),
        
        ],style={'backgroundColor': '#0066CC'},width=2),

        dbc.Col([
            html.Div(
                dcc.Tabs(id="tabs", children=[
                    dcc.Tab(label='3-Dimensions', children=[
                        html.Div([
                            dcc.Graph(id="threeD",
                            config = {'toImageButtonOptions':
                                    {'width': None,
                                    'height': None,
                                    'format': 'png',
                                    'filename': '3D_Plot'}
                                }
                            )
                        ]),
                    ]),
                    dcc.Tab(label='2-Dimensions', children=[
                        html.Div(
                            dcc.RadioItems(
                                id='bestfit',
                                options=[{'label': i, 'value': i} for i in ['Best-Fit','Scatter']],
                                value='Best-Fit',
                                labelStyle={"padding-right":"10px","margin":"auto"},
                                style={"text-align":"center"}
                            )
                        ),
                        html.Div([
                            dcc.Graph(id="twoD",
                            config = {'toImageButtonOptions':
                                {'width': None,
                                'height': None,
                                'format': 'png',
                                'filename': '2D_Plot'}
                            })
                        ])
                    ]),
                    dcc.Tab(label='Table', children=[
                        dt.DataTable(
                            id='table',
                            page_current=0,
                            page_size=75,
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                            style_table={'height': "87vh",'min-height': "87vh"},
                            fixed_rows={'headers': True}
                        )
                    ])
                ]),style={'width':"100%",'height':'100%', 'backgroundColor': 'white'}
            )
        ])
    ],style={"height":"100vh"},no_gutters=True),
        
    html.Details([
            html.Summary('Comparable Graphs',style={"cursor":"pointer"}),
            dbc.Row([
                dbc.Col([
                    html.Div([html.H1("Graph 1")],style={'text-align':"center", "margin-left":"auto","margin-right":"auto", 'color':"white","padding-top":"30%"}),

                    html.Div(dcc.Dropdown(id="select-xaxis2", placeholder = "Select x-axis", value = "Temperature (C)",
                        options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                    html.Div(dcc.Dropdown(id="select-yaxis2", placeholder = "Select y-axis", value = "Pressure (Psi)",
                        options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                    html.Div(dcc.Dropdown(id="select-zaxis2", placeholder = "Select z-axis", value = "Halflife (Min)",
                        options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                    html.Div([html.H1("Graph 2")],style={'text-align':"center", "margin-left":"auto","margin-right":"auto", "padding-top":"70%", 'color':"white"}),

                    html.Div(dcc.Dropdown(id="select-xaxis3", placeholder = "Select x-axis", value = "Temperature (C)",
                        options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                    html.Div(dcc.Dropdown(id="select-yaxis3", placeholder = "Select y-axis", value = "Pressure (Psi)",
                        options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                    html.Div(dcc.Dropdown(id="select-zaxis3", placeholder = "Select z-axis", value = "Halflife (Min)",
                        options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                        style={"margin-left": "auto", "margin-right": "auto", "width": "80%"}),
                ],style={'backgroundColor': '#0066CC'},width=2),
              
                dbc.Col([
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                dcc.Graph(id="comp1",
                                config = {'toImageButtonOptions':
                                    {'width': None,
                                    'height': None,
                                    'format': 'png',
                                    'filename': '3D_Plot_Comp1'}
                                })
                            ])
                        ),

                        dbc.Col(
                            html.Div([
                                dcc.Graph(id="comp2",
                                config = {'toImageButtonOptions':
                                    {'width': None,
                                    'height': None,
                                    'format': 'png',
                                    'filename': '3D_Plot_Comp2'}
                                })
                            ])
                        )
                    ],no_gutters=True),

                    dbc.Row([
                        dbc.Col(
                            dt.DataTable(
                                id='comp1table',
                                page_current=0,
                                page_size=75,
                                export_format='xlsx',
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                                style_table={"height":"20vh","min-height":"20vh"},
                                fixed_rows={'headers': True},
                            ),style={"padding-left":20,"padding-right":20}
                        ),

                        dbc.Col(
                            dt.DataTable(
                                id='comp2table',
                                page_current=0,
                                page_size=75,
                                columns=[{'id': c, 'name': c} for c in dv.columns[7:]],
                                export_format='xlsx',
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                                style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                                style_table={"height":"20vh","min-height":"20vh"},
                                fixed_rows={'headers': True},
                            ),style={"padding-left":20,"padding-right":20}
                        )
                    ],no_gutters=True)  
                ])
            ],style={"height":"100vh"},no_gutters=True),
    ],style={"text-align":"center"})
])

about = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Link('Home', href='/',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18}),
            width=3
        ),
        dbc.Col([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='About Us', children=[
                    html.Br(),
                    html.H1("Team",style={"text-align":"center"}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Ren.PNG", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Fei Ren", className="card-title"),
                                        html.Hr(),
                                        html.H6("Associate Professor"),
                                        html.A("renfei@temple.edu", href="mailto: renfei@temple.edu"),
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),
                            
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Thakore.PNG", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Virensinh Thakore", className="card-title"),
                                        html.Hr(),
                                        html.H6("Ph.D Candidate"),
                                        html.A("thakorev@temple.edu", href="mailto: thakorev@temple.edu"),
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Voytek.jpg", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Josh Voytek", className="card-title"),
                                        html.Hr(),
                                        html.H6("Web Developer"),
                                        html.A("josh.voytek@temple.edu", href="mailto: josh.voytek@temple.edu"),
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),
                    ],style={"margin-left":"auto","margin-right":"auto","width":"80%"},no_gutters=True),
                    html.Br(),
                    html.P("Email Virensinh or Josh from above with related research data not currently being displayed."
                    ,style={"font-size":23,"padding-left":30,"padding-right":30,"text-align":"center"})         
                ]),
                dcc.Tab(label='About The Project', children=[
                    html.Br(),
                    html.H1("Project",style={"text-align":"center"}),
                    html.Br(),
                    html.Div([

                        html.P("This project is supported by the Geothermal Technology Office of the Department of Energy and the Oak Ridge National Laboratory.",
                        style={"font-size":23,"padding-left":30,"padding-right":30}),

                        html.P("Hydraulic fracturing is the process of fracturing rock formations with high-pressure water-based fluids. In Enhanced Geothermal " +
                           "Systems (EGS) hydraulic fracturing is carried out by injecting high-pressure fluids into the Hot Dry Rocks (HDR) under carefully " +
                           "controlled conditions. The fluid used for fracturing is an important component for EGS, not only concerning the technical approch but " +
                           "also environmental impact. Recent research has been carried out to develop waterless fracturing technologies for EGS, including foambased hydrofracking, " +
                           "where foams are mixtures of gas and liquid fluids. Foam fracturing fluids have potential benefits over water-based " +
                           "fluids because of less water consumption, less damage in water sensitive formations, and less liquid to recover and handle after " +
                           "fracturing process. One challenge for implementing foam fracturing in EGS is to achieve stable foams at high temperatures, as the foam " +
                           "stability tends to decay with increase in temperature. The intent of this project is to compile and neatly display modern literature data on foambased hydrofracking for EGS.",
                            style={"font-size":23,"padding-left":50,"padding-right":50}
                        )
                        
                    ],style={"text-align":"center"}),
                    html.P("Last Updated: " + today,style={"text-align":"center"})
                ]),
            ]),
        ],style={"backgroundColor":"white"}),
        dbc.Col(style={'backgroundColor': '#0066CC',"height":"100vh"},width=3)
    ],style={'backgroundColor': '#0066CC',"height":"100%"},no_gutters=True)
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        return about
    else:
        return home

@app.callback(
    Output('controls-container', 'style'),
    [Input('toggle', 'value')])

def toggle_container(toggle_value):
    if toggle_value == 'Show More':
        return {'display': 'block','max-height':600,'overflow-y':'auto',"border-top":"1px black solid"}
    else:
        return {'display': 'none'}

@app.callback(
    [Output("table", "data"),
     Output("table", "columns")],
    [Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_table(ga, sur, surc, add, addc, lp):
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    return (
        cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns[:]],
    )

@app.callback(
    Output('table', 'style_data_conditional'),
    [Input("select-xaxis", "value"),
     Input("select-yaxis", "value"),
     Input("select-zaxis", "value")]
)
def update_styles(x,y,z):
    return [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': { 'column_id': x },
        'background_color': '#0066CC',
        'color': 'white',
    },
    {
        'if': { 'column_id': y },
        'background_color': '#0066CC',
        'color': 'white',
    },
    {
        'if': { 'column_id': z },
        'background_color': '#0066CC',
        'color': 'white',
    }]

@app.callback(
    Output("twoD", "figure"),
    [Input("select-xaxis", "value"),
     Input("select-yaxis", "value"),
     Input("bestfit", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_twoD(selected_x, selected_y, fit, ga, sur, surc, add, addc, lp):
    check = 0
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    data = []
    names = list(dict.fromkeys(dv['Study']))

    for i in names:
        check = 0
        name_array = cleaned[cleaned.Study == i]
        for x in name_array[selected_x]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_y]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue

        name_array.sort_values(by=[selected_x], inplace=True)

        if(fit == 'Scatter'):
            trace = go.Scatter(y=name_array[selected_y], x=name_array[selected_x], hovertext= "Study: " + name_array.Study + "<br />Gas: "
            + name_array.Gas + "<br />Surfactant: " + name_array.Surfactant + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"] + "<br />Additive: "
            + name_array.Additive + "<br />Concentration Additive: " + name_array['Additive Concentration'] + "<br />Liquid Phase: " + name_array.LiquidPhase,
            hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8},name=i)

        if(fit == 'Best-Fit'):
            m, b = np.polyfit(name_array[selected_x].values.astype(float),name_array[selected_y].values.astype(float), 1)
            correlation_matrix = np.corrcoef(name_array[selected_x].values.astype(float), name_array[selected_y].values.astype(float))
            correlation_xy = correlation_matrix[0,1]
            r_squared = correlation_xy**2

            trace = go.Scatter(y=m*name_array[selected_x].values+b, x=name_array[selected_x],mode='lines+markers',name=i
            ,hovertext= "Study: " + name_array.Study + "<br />Slope: " + str(round(m,2)) + "<br />Intercept " + str(round(b,2)) + "<br />R Squared " + str(round(r_squared,2)),
            hoverinfo='text')
            
        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            yaxis={
                "title":selected_y,
                "titlefont_size":20,
                "tickfont_size":18,
            },
            xaxis={
                "title":selected_x,
                "titlefont_size":20,
                "tickfont_size":18
            },
            legend={
                    "font_size": 24,
            },
            font={
                "family":"Times New Roman",
            },
            hovermode="closest",
            height=750,
        )
    }

@app.callback( #updates the 3d graph
    Output("threeD", "figure"),
    [Input("select-xaxis", "value"),
     Input("select-yaxis", "value"),
     Input("select-zaxis", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_threeD(selected_x, selected_y, selected_z, ga, sur, surc, add, addc, lp):
    check = 0
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    data = []
    names = list(dict.fromkeys(dv['Study']))

    for i in names:
        check = 0
        name_array = cleaned[cleaned.Study == i]
        for x in name_array[selected_x]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_y]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_z]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        trace = go.Scatter3d(y=name_array[selected_y], x=name_array[selected_x],z=name_array[selected_z], hovertext= "Study: " + name_array.Study + "<br />Gas: "
        + name_array.Gas + "<br />Surfactant: " + name_array.Surfactant + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"] + "<br />Additive: "
        + name_array.Additive + "<br />Concentration Additive: " + name_array['Additive Concentration'] + "<br />Liquid Phase: " + name_array.LiquidPhase,
        hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8},name=i)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=850,
                legend={
                    "font_size": 24,
                },
                font={
                    "size": 16,
                    "family": "Times New Roman",
                },
                scene={
                    "camera":{"center":dict(x=0.05,y=0,z=-0.25)},
                    "xaxis": {"title": f"{selected_x.title()}"},
                    "yaxis": {"title": f"{selected_y.title()}"},
                    "zaxis": {"title": f"{selected_z.title()}"}
                }
            )}

@app.callback( #updates the 3d graph
    Output("comp1", "figure"),
    [Input("select-xaxis2", "value"),
     Input("select-yaxis2", "value"),
     Input("select-zaxis2", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_comp1(selected_x, selected_y, selected_z, ga, sur, surc, add, addc, lp):
    check = 0
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    data = []
    names = list(dict.fromkeys(dv['Study']))

    for i in names:
        check = 0
        name_array = cleaned[cleaned.Study == i]
        for x in name_array[selected_x]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_y]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_z]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        trace = go.Scatter3d(y=name_array[selected_y], x=name_array[selected_x],z=name_array[selected_z], hovertext= "Study: " + name_array.Study + "<br />Gas: "
        + name_array.Gas + "<br />Surfactant: " + name_array.Surfactant + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"] + "<br />Additive: "
        + name_array.Additive + "<br />Concentration Additive: " + name_array['Additive Concentration'] + "<br />Liquid Phase: " + name_array.LiquidPhase,
        hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8},name=i)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=680,
                legend={
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "valign":"middle",
                    "font_size": 24,
                },
                font={
                    "size": 16,
                    "family": "Times New Roman",
                },
                scene={
                    "camera":{"center":dict(x=0.05,y=0,z=-0.25)},
                    "xaxis": {"title": f"{selected_x.title()}"},
                    "yaxis": {"title": f"{selected_y.title()}"},
                    "zaxis": {"title": f"{selected_z.title()}"}
                },
                margin={
                    "b":0
                }
            )}

@app.callback(
    [Output("comp1table", "data"),
     Output("comp1table", "columns")],
    [Input("select-xaxis2", "value"),
     Input("select-yaxis2", "value"),
     Input("select-zaxis2", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_comp1table(selected_x, selected_y,selected_z, ga, sur, surc, add, addc, lp):
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    cleaned = cleaned[cleaned[selected_x] != "None"]
    cleaned = cleaned[cleaned[selected_y] != "None"]
    cleaned = cleaned[cleaned[selected_z] != "None"]

    final = cleaned.columns
    final = final.drop([selected_x,selected_y,selected_z])
    cleaned = cleaned.drop(final, axis=1)

    return (
        cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]
    )

@app.callback( #updates the 3d graph
    Output("comp2", "figure"),
    [Input("select-xaxis3", "value"),
     Input("select-yaxis3", "value"),
     Input("select-zaxis3", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_comp2(selected_x, selected_y, selected_z, ga, sur, surc, add, addc, lp):
    check = 0
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    data = []
    names = list(dict.fromkeys(dv['Study']))

    for i in names:
        check = 0
        name_array = cleaned[cleaned.Study == i]
        for x in name_array[selected_x]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_y]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        for x in name_array[selected_z]:
            if x == "None":
                check = 1 
                break
        if check == 1:
            continue
        trace = go.Scatter3d(y=name_array[selected_y], x=name_array[selected_x],z=name_array[selected_z], hovertext= "Study: " + name_array.Study + "<br />Gas: "
        + name_array.Gas + "<br />Surfactant: " + name_array.Surfactant + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"] + "<br />Additive: "
        + name_array.Additive + "<br />Concentration Additive: " + name_array['Additive Concentration'] + "<br />Liquid Phase: " + name_array.LiquidPhase,
        hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8},name=i)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=680,
                legend={
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "valign":"middle",
                    "font_size": 24,
                },
                font={
                    "size": 16,
                    "family": "Times New Roman",
                },
                scene={
                    "camera":{"center":dict(x=0.05,y=0,z=-0.25)},
                    "xaxis": {"title": f"{selected_x.title()}"},
                    "yaxis": {"title": f"{selected_y.title()}"},
                    "zaxis": {"title": f"{selected_z.title()}"}
                },
                margin={
                    "b":0
                }
            )}

@app.callback( #updates 2d graph relative to selected axes and checklist data
    [Output("comp2table", "data"),
     Output("comp2table", "columns")],
    [Input("select-xaxis3", "value"),
     Input("select-yaxis3", "value"),
     Input("select-zaxis3", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_comp2table(selected_x, selected_y,selected_z, ga, sur, surc, add, addc, lp):
    cl = dv[dv['Gas'].isin(ga)]
    ea = cl[cl['Surfactant'].isin(sur)]
    n = ea[ea["Surfactant Concentration"].isin(surc)]
    e = n[n['Additive'].isin(add)]
    d = e[e['Additive Concentration'].isin(addc)]
    cleaned = d[d['LiquidPhase'].isin(lp)]

    cleaned = cleaned[cleaned[selected_x] != "None"]
    cleaned = cleaned[cleaned[selected_y] != "None"]
    cleaned = cleaned[cleaned[selected_z] != "None"]

    final = cleaned.columns
    final = final.drop([selected_x,selected_y,selected_z])
    cleaned = cleaned.drop(final, axis=1)

    return (
        cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]
    )

if __name__ == '__main__':
    app.run_server(debug=True)