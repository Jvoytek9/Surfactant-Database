import os
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[
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

dv.dropna(
    axis=0,
    how='all',
    thresh=None,
    subset=None,
    inplace=True
)

dv.fillna("None", inplace=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

home = html.Div([
    html.Div(
        [html.Div([html.P("Foam Database")],
                  style={'text-align':"center", 'position':"absolute", 'width':'15%', 'top':0, 'left':0, 'right':0,
                  'bottom':0, "padding-top": 40, 'color':"white", "font-size":40}),

         html.Div(dcc.Dropdown(id="select-xaxis", placeholder = "Select x-axis", value = "Temperature (C)",
            options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

         html.Div(dcc.Dropdown(id="select-yaxis", placeholder = "Select y-axis", value = "Pressure (Psi)",
            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

         html.Div(dcc.Dropdown(id="select-zaxis", placeholder = "Select z-axis", value = "Halflife (Min)",
            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%","padding-bottom":10}),

        html.Div([
            html.Div([
                html.Div([dcc.RadioItems(
                    id='toggle',
                    options=[{'label': i, 'value': i} for i in ['Show More', 'Show Less']],
                    value='Show Less'
                )],style={"text-align":"center","font-size":14})
            ],style={"height":20}),

            html.Div(id='controls-container', children=[

                html.Details([
                    html.Summary("Gasses"),
                html.Div(dcc.Checklist(
                                id = 'gasses',
                                options= [{'label': gas, 'value': gas} for gas in list(dict.fromkeys(dv['Gas']))],
                                value = list(dict.fromkeys(dv['Gas'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),

                html.Details([
                    html.Summary("Surfactants"),
                html.Div(dcc.Checklist(
                                id = 'surfactants',
                                options= [{'label': surfactant, 'value': surfactant} for surfactant in list(dict.fromkeys(dv['Surfactant']))],
                                value = list(dict.fromkeys(dv['Surfactant'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),

                html.Details([
                    html.Summary("Surfactant Concentrations"),
                html.Div(dcc.Checklist(
                                id = 'sconc',
                                options= [{'label': sc, 'value': sc} for sc in list(dict.fromkeys(dv['Surfactant Concentration']))],
                                value = list(dict.fromkeys(dv['Surfactant Concentration'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),

                html.Details([
                    html.Summary("Additives"),
                html.Div(dcc.Checklist(
                                id = 'additives',
                                options= [{'label': ad, 'value': ad} for ad in list(dict.fromkeys(dv['Additive']))],
                                value = list(dict.fromkeys(dv['Additive'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),

                html.Details([
                    html.Summary("Additive Concentrations"),
                html.Div(dcc.Checklist(
                                id = 'aconc',
                                options= [{'label': adc, 'value': adc} for adc in list(dict.fromkeys(dv['Additive Concentration']))],
                                value = list(dict.fromkeys(dv['Additive Concentration'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),

                html.Details([
                    html.Summary("Liquid Phase"),
                html.Div(dcc.Checklist(
                                id = 'lp',
                                options= [{'label': li, 'value': li} for li in list(dict.fromkeys(dv['LiquidPhase']))],
                                value = list(dict.fromkeys(dv['LiquidPhase'])),
                                labelStyle={'display': 'block'})),
                ],style={"padding-top":15}),
                ],style={"display":"none"}),
            ], style={"text-align":"center", "position":"relative", "display": "block", "margin-left": "auto",
                    "margin-right": "auto", "width": "80%", "left":0, "bottom":10, "backgroundColor": 'white', "border-radius":3}),

         ], id="wrapper", style={"left":0, "display": "inline-block", "margin-left": "auto",
                "margin-right": "auto","margin-top": "auto", "width": "15%", "padding-top":180}),

    dcc.Link('About', href='/about',style={'position':'absolute','top':5, 'left':5,"color":"white"}),

    html.Div(
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='3-Dimensions', children=[
                html.Div([dcc.Graph(id="threeD")]),
            ]),
            dcc.Tab(label='2-Dimensions', children=[
                html.Div([dcc.Graph(id="twoD")])
            ]),
            dcc.Tab(label='Table', children=[
                dt.DataTable(
                    id='table',
                    page_current=0,
                    page_size=75,
                    style_cell={'whiteSpace': 'normal','height': 'auto','maxWidth':'0', 'textAlign': 'left'},
                    style_data={'whiteSpace': 'normal','height': 'auto'},
                    style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                    }],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    fixed_rows={'headers': True, 'data': 0 },
                    style_table={'whiteSpace': 'normal',
                        'height': 835,'min-height': 835},
                ),
            ])
        ]),style = {'position':"absolute",'width':"85%",'height':'100%', "display":"inline-block",'backgroundColor': 'white'}),
                html.Details([
                    html.Summary('Comparable Graphs',style={"cursor":"pointer"}),

                        html.Div([
                            html.Div([html.P("Graph 1")],style={'text-align':"center", 'position':"absolute", 'top':0, 'left':0, 'right':0,
                            'bottom':0, "padding-top": 55, 'color':"white", "font-size":40}),

                         html.Div(dcc.Dropdown(id="select-xaxis2", placeholder = "Select x-axis", value = "Temperature (C)",
                            options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                                  style={"padding-top":170,"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                         html.Div(dcc.Dropdown(id="select-yaxis2", placeholder = "Select y-axis", value = "Pressure (Psi)",
                            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                         html.Div(dcc.Dropdown(id="select-zaxis2", placeholder = "Select z-axis", value = "Halflife (Min)",
                            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%", "padding-bottom":10}),

                         html.Div([html.P("Graph 2")],style={'text-align':"center", 'position':"absolute", 'left':0, 'right':0,
                            'bottom':0, "padding-bottom": 310, 'color':"white", "font-size":40}),

                         html.Div(dcc.Dropdown(id="select-xaxis3", placeholder = "Select x-axis", value = "Temperature (C)",
                            options=[{'label': i.title(), 'value': i}  for i in dv.columns[7:]], clearable=False),
                                  style={"padding-top":230,"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                         html.Div(dcc.Dropdown(id="select-yaxis3", placeholder = "Select y-axis", value = "Pressure (Psi)",
                            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%"}),

                         html.Div(dcc.Dropdown(id="select-zaxis3", placeholder = "Select z-axis", value = "Halflife (Min)",
                            options=[{'label': i.title(), 'value': i} for i in dv.columns[7:]], clearable=False),
                                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "80%", "padding-bottom":10}),

                        ],style={"text-align":"left","font-size":16,'position':"absolute", 'top':21, 'left':0,'backgroundColor': '#0066CC', 'width':'15%', 'height':832}),

                        html.Div([
                            html.Div([
                                html.Div([dcc.Graph(id="comp1")]),
                            ],style = {'width':"50%","display":"inline-block",'backgroundColor': 'white'}),
                            html.Div([
                                html.Div([dcc.Graph(id="comp2")]),
                            ],style = {'width':"50%", "display":"inline-block",'backgroundColor': 'white'}),

                            html.Div([
                                dt.DataTable(
                                    id='comp1table',
                                    page_current=0,
                                    page_size=75,
                                    export_format='xlsx',
                                    style_cell={'whiteSpace': 'normal','height': 'auto','font-size':12, "text-align":"left"},
                                    style_data={'whiteSpace': 'normal','height': 'auto'},
                                    style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(248, 248, 248)'
                                    }],
                                    style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                                    fixed_rows={'headers': True, 'data': 0 },
                                    style_table={'whiteSpace': 'normal','height': 175},
                                ),
                            ],style = {'position':'absolute','top':'90%','left':"5%",'width':"40%",'backgroundColor': 'white','text-align':'right'}),
                            html.Div([
                                dt.DataTable(
                                    id='comp2table',
                                    page_current=0,
                                    page_size=75,
                                    columns=[{'id': c, 'name': c} for c in dv.columns[7:]],
                                    export_format='xlsx',
                                    style_cell={'whiteSpace': 'normal','height': 'auto','font-size':12, "text-align":"left"},
                                    style_data={'whiteSpace': 'normal','height': 'auto',},
                                    style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(248, 248, 248)'
                                    }],
                                    style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                                    fixed_rows={'headers': True, 'data': 0 },
                                    style_table={'whiteSpace': 'normal','height': 175},
                                ),
                            ],style = {'position':'absolute','top':'90%','right':"5%",'width':"40%",'backgroundColor': 'white','text-align':'right'}),
                        ],style={'position':'absolute','right':0,'width':"85%"})

                ],style={'position':"absolute", 'top':'100%',"text-align":"center","font-size":18,'width':"100%"})

],style={'position':"absolute", 'top':0, 'left':0,'backgroundColor': '#0066CC', 'width':"100%", 'height':"100%"})

about = html.Div([
    html.Div(
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='About Us', children=[
                html.Br(),
                html.H1("Team"),
                html.Div([
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardImg(src="/assets/Ren.png", top=True,style={"height":"25vh","width":"100%"}),
                            dbc.CardBody(
                                [
                                    html.H5("Dr.Fei Ren", className="card-title"),
                                    html.A("renfei@temple.edu", href="mailto: renfei@temple.edu"),
                                ])
                        ])),

                        dbc.Col(dbc.Card([
                            dbc.CardImg(src="/assets/Thakore.png", top=True,style={"height":"25vh","width":"100%"}),
                            dbc.CardBody(
                                [
                                    html.H5("Virensinh Thakore", className="card-title"),
                                    html.A("thakorev@temple.edu", href="mailto: thakorev@temple.edu"),
                                ])
                        ]))
                    ],style={"margin-left":"auto","margin-right":"auto","width":"60%"}),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardImg(src="/assets/Voytek.jpg", top=True,style={"height":"25vh","width":"100%"}),
                            dbc.CardBody(
                                [
                                    html.H5("Josh Voytek", className="card-title"),
                                    html.A("josh.voytek@temple.edu", href="mailto: josh.voytek@temple.edu"),
                                ])
                        ])),
                    ],style={"margin-left":"auto","margin-right":"auto","width":"30%"})],
                style={"width":"100%"})

                
            ]),
            dcc.Tab(label='About The Project', children=[
                html.Br(),
                html.H1("Project"),
            ]),
        ]),
    style={"height": "100%","width":"50%","margin-left":"auto","margin-right":"auto",'backgroundColor': 'white','text-align':'center'}),
    
    dcc.Link('Home', href='/',style={'position':'absolute','top':5, 'left':5,"color":"white"}),

],style={"position":"absolute","left":0,"top":0,'backgroundColor': '#0066CC', 'width':"100%", 'height':"100%"})

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
        return {'display': 'block','max-height':500,'overflow-y':'auto',"border-top":"1px black solid"}
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
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value'),
     Input('additives', 'value'),
     Input('aconc', 'value'),
     Input('lp', 'value')],
)
def update_twoD(selected_x, selected_y, ga, sur, surc, add, addc, lp):
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
        trace = go.Scatter(y=name_array[selected_y], x=name_array[selected_x], hovertext= "Study: " + name_array.Study + "<br />Gas: "
        + name_array.Gas + "<br />Surfactant: " + name_array.Surfactant + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"] + "<br />Additive: "
        + name_array.Additive + "<br />Concentration Additive: " + name_array['Additive Concentration'] + "<br />Liquid Phase: " + name_array.LiquidPhase,
        hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8},name=i)
        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            yaxis=dict(
                title=selected_y,
                titlefont_size=20,
                tickfont_size=18,
            ),
            xaxis=dict(
                title=selected_x,
                titlefont_size=20,
                tickfont_size=18
            ),
            legend=dict(
                font_size = 20,
            ),
            font=dict(
                family="Times New Roman",
            ),
            hovermode="closest",
            height=790,
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
        name_array.sort_values(by=[selected_x], inplace=True)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=800,
                legend=dict(
                    font_size = 24,
                ),
                font=dict(
                    size = 16,
                    family="Times New Roman",
                ),
                scene={"aspectmode": "cube",
                        "camera":{"center":dict(x=0.05,y=0,z=-0.15)},
                        "xaxis": {"title": f"{selected_x.title()}"},
                        "yaxis": {"title": f"{selected_y.title()}"},
                        "zaxis": {"title": f"{selected_z.title()}"}})
            }

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
        name_array.sort_values(by=[selected_x], inplace=True)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=700,
                title="Graph 1",
                scene={"aspectmode": "cube",
                        "camera":{"center":dict(x=0.05,y=0,z=-0.25)},
                        "xaxis": {"title": f"{selected_x.title()}"},
                        "yaxis": {"title": f"{selected_y.title()}"},
                        "zaxis": {"title": f"{selected_z.title()}"}})
            }

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
        name_array.sort_values(by=[selected_x], inplace=True)
        data.append(trace)

    return {"data": data,
            "layout": go.Layout(
                height=700,
                title="Graph 2",
                scene={"aspectmode": "cube",
                        "camera":{"center":dict(x=0.05,y=0,z=-0.25)},
                        "xaxis": {"title": f"{selected_x.title()}"},
                        "yaxis": {"title": f"{selected_y.title()}"},
                        "zaxis": {"title": f"{selected_z.title()}"}})
            }

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