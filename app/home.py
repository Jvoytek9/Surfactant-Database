import numpy as np
import pandas as pd
np.warnings.filterwarnings('ignore')
from scipy.optimize import curve_fit
#pylint: disable=unbalanced-tuple-unpacking
#pylint: disable=unused-variable

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.graph_objs as go

from initialize_data import Return_Data, unique_studies, unique_gasses, unique_surfactants, unique_surfconcs, unique_additives, unique_addconcs, unique_liquidphase

dv = Return_Data()

Graph_Height = 605

home = dbc.Row([
    dbc.Col([
        html.Div([
            html.Div([html.H1("Graph 2")],style={'text-align':"center", "margin-left":"auto","margin-right":"auto", 'color':"white"}),
            dbc.Row([
                dbc.Col(html.H6("X: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-xaxis2", placeholder = "Select x-axis", value = "Temperature (C)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis2", placeholder = "Select y-axis", value = "Halflife (Min)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dbc.Col(html.H6("Z: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-zaxis2", placeholder = "Select z-axis", value = "Pressure (Psi)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dcc.RadioItems(
                    id='toggle2',
                    options=[{'label': i, 'value': i} for i in ['Show Less','Show More']],
                    value='Show Less',
                    labelStyle={"padding-right":"10px","margin":"auto"},
                    style={"text-align":"center","margin":"auto"}
                ),
            ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto"}),

            html.Div([
                html.Div(id='controls-container2', children=[
                    html.Hr(),

                    html.H5("Configurations:"),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Formatting"),
                        html.Div(
                            dcc.Checklist(
                                id='normalize2',
                                options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y','Normalize Z','Average Y-axis']],
                                value=[],
                                labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                            )
                        ,style={"margin":"auto"})
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Fitting"),
                        html.Div(
                            dcc.Checklist(
                                id = 'bestfit2',
                                options= [{'label': i, 'value': i} for i in ['Scatter','Line','Poly-Fit','Log-Fit','Exp-Fit',"Power-Fit"]],
                                value = ['Scatter'],
                                labelStyle={"padding-right":"10px","margin":"auto"}
                            )
                        ,style={"margin":"auto"}),

                        html.Div([
                            html.H6("Degree:",style={"padding-top":"10px"}),
                            dcc.Slider(
                                id="input_fit2",
                                max=3,
                                min=1,
                                value=1,
                                step=1,
                                included=False,
                                marks={
                                    1: {'label': '1'},
                                    2: {'label': '2'},
                                    3: {'label': '3'}
                                }
                            )
                        ])
                    ]),

                html.Hr(),

                html.H5("Filter By:"),

                html.Hr(),

                html.Details([
                    html.Summary("Study"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allstudies2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallstudies2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'studies2',
                        options= [{'label': study, 'value': study} for study in unique_studies],
                        value = unique_studies,
                        labelStyle={'display': 'block'}
                    )
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Gas Used"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allgas2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallgas2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'gasses2',
                        options= [{'label': gas, 'value': gas} for gas in unique_gasses],
                        value = unique_gasses,
                        labelStyle={'display': 'block'}
                    )
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Surfactant"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsurf2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsurf2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'surfactants2',
                        options= [{'label': surfactant, 'value': surfactant} for surfactant in unique_surfactants],
                        value = unique_surfactants,
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Surfactant Concentration"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'sconc2',
                        options= [{'label': sc, 'value': sc} for sc in unique_surfconcs],
                        value = unique_surfconcs,
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Additive"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='alladd2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dalladd2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'additives2',
                        options= [{'label': ad, 'value': ad} for ad in unique_additives],
                        value = unique_additives,
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Additive Concentration"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allaconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallaconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'aconc2',
                        options= [{'label': adc, 'value': adc} for adc in unique_addconcs],
                        value = unique_addconcs,
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Liquid Phase"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='alllp2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dalllp2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'lp2',
                        options= [{'label': li, 'value': li} for li in unique_liquidphase],
                        value = unique_liquidphase,
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),


        ],id="compare_dropdown",style={"display":"None"}),

        html.Div([html.H1("Foam Database")],
            style={'text-align':"center", "margin-right":"auto","margin-left":"auto", 'color':"white","width": "80%","padding-top":"20%"}),

        html.Div([
            html.Div(
                dcc.RadioItems(
                    id='addComp',
                    options=[{'label': i, 'value': i} for i in ['No Compare','Compare']],
                    value='No Compare',
                    labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px","color":"white"}
                )
            ,style={"margin":"auto"}),

            dbc.Row([
                dbc.Col(html.H6("X: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-xaxis", placeholder = "Select x-axis", value = "Pressure (Psi)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),


            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis", placeholder = "Select y-axis", value = "Halflife (Min)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),


            dbc.Row([
                dbc.Col(html.H6("Z: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-zaxis", placeholder = "Select z-axis", value = "Temperature (C)",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[7:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

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

                    html.H5("Configurations:"),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Formatting"),
                        html.Div(
                            dcc.Checklist(
                                id='normalize',
                                options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y','Normalize Z','Average Y-axis']],
                                value=[],
                                labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                            )
                        ,style={"margin":"auto"})
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Fitting"),
                        html.Div(
                            dcc.Checklist(
                                id = 'bestfit',
                                options= [{'label': i, 'value': i} for i in ['Scatter','Line','Poly-Fit','Log-Fit','Exp-Fit',"Power-Fit"]],
                                value = ['Scatter'],
                                labelStyle={"padding-right":"10px","margin":"auto"}
                            )
                        ,style={"margin":"auto"}),

                        html.Div([
                            html.H6("Degree:",style={"padding-top":"10px"}),
                            dcc.Slider(
                                id="input_fit",
                                max=3,
                                min=1,
                                value=1,
                                step=1,
                                included=False,
                                marks={
                                    1: {'label': '1'},
                                    2: {'label': '2'},
                                    3: {'label': '3'}
                                }
                            )
                        ])
                    ]),

                    html.Hr(),

                    html.H5("Filter By:"),

                    html.Hr(),

                    html.Details([
                        html.Summary("Study"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='allstudies', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dallstudies', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'studies',
                            options= [{'label': study, 'value': study} for study in unique_studies],
                            value = unique_studies,
                            labelStyle={'display': 'block'}
                        )
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Gas Used"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='allgas', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dallgas', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'gasses',
                            options= [{'label': gas, 'value': gas} for gas in unique_gasses],
                            value = unique_gasses,
                            labelStyle={'display': 'block'}
                        )
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Surfactant"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='allsurf', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dallsurf', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'surfactants',
                            options= [{'label': surfactant, 'value': surfactant} for surfactant in unique_surfactants],
                            value = unique_surfactants,
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Surfactant Concentration"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='allsconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dallsconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'sconc',
                            options= [{'label': sc, 'value': sc} for sc in unique_surfconcs],
                            value = unique_surfconcs,
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Additive"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='alladd', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dalladd', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'additives',
                            options= [{'label': ad, 'value': ad} for ad in unique_additives],
                            value = unique_additives,
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Additive Concentration"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='allaconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dallaconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'aconc',
                            options= [{'label': adc, 'value': adc} for adc in unique_addconcs],
                            value = unique_addconcs,
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Liquid Phase"),

                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Select All', id='alllp', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-right":"5px"}),

                            dbc.Col(
                                dbc.Button('Deselect All', id='dalllp', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                            ,style={"padding-left":"5px"}),
                        ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                        dcc.Checklist(
                            id = 'lp',
                            options= [{'label': li, 'value': li} for li in unique_liquidphase],
                            value = unique_liquidphase,
                            labelStyle={'display': 'block'}
                        ),
                    ]),

                    html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),

        ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto", "width": "100%"}),

        dcc.Link('About', href='/about',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18})

    ],style={'backgroundColor': '#9E1B34','width':'20%'}),

    dbc.Col([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='3-Dimensions', children=[
                dbc.Row([
                    dbc.Col([
                            dcc.Graph(id="comp1_3D_graph",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': '3D_Plot_Comp1'}
                            })
                    ],style={"width":"50%"}),

                    dbc.Col([
                            dcc.Graph(id="comp2_3D_graph",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': '3D_Plot_Comp2'}
                            })
                    ],id="compare_graph",style={"display":"None","width":"50%"})
                ],no_gutters=True),

                dbc.Row([
                    dbc.Col(
                        dt.DataTable(
                            id='comp1_3D_table',
                            page_current=0,
                            page_size=75,
                            export_format='xlsx',
                            style_data_conditional=[
                            {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                            style_table={'max-height': "20vh", "height": "20vh"},
                            fixed_rows={'headers': True},
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        ),
                    style={"padding-left":20,"padding-right":20,"width":"50%"}),

                    dbc.Col(
                        dt.DataTable(
                            id='comp2_3D_table',
                            page_current=0,
                            page_size=75,
                            columns=[{'id': c, 'name': c} for c in dv.columns[7:]],
                            export_format='xlsx',
                            style_data_conditional=[
                            {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                            style_table={'max-height': "20vh", "height": "20vh"},
                            fixed_rows={'headers': True},
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        )
                    ,style={"display":"None","width":"50%"},id="compare_table")
                ],no_gutters=True)
            ]),

            dcc.Tab(label='2-Dimensions', children=[
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            dcc.Graph(id="comp1_2D_graph",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': '2D_Plot_Comp1'}
                            })
                        ])
                    ,style={"width":"50%"}),

                    dbc.Col(
                        html.Div([
                            dcc.Graph(id="comp2_2D_graph",
                                config = {'toImageButtonOptions':
                                {'width': None,
                                'height': None,
                                'format': 'png',
                                'filename': '2D_Plot_Comp2'}
                                })
                            ])
                    ,id="compare_graph_2D",style={"display":"None","width":"50%"})
                ],no_gutters=True),

                dbc.Row([
                    dbc.Col(
                        dt.DataTable(
                            id='comp1_2D_table',
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
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        ),style={"padding-left":20,"padding-right":20,"width":"50%"}
                    ),

                    dbc.Col(
                        dt.DataTable(
                            id='comp2_2D_table',
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
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        )
                    ,style={"display":"None","width":"50%"},id="compare_table_2D")
                ],no_gutters=True)
            ]),

            dcc.Tab(label='Table', children=[
                dt.DataTable(
                    id='table',
                    data = dv.to_dict('records'),
                    columns = [{'id': c, 'name': c} for c in dv.columns[:-1]],
                    page_current=0,
                    page_size=75,
                    style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                    }],
                    style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                        'whiteSpace': 'normal'
                    },
                    style_table={
                        'height': "87vh",
                        'min-height': "87vh",
                        'overflowY': 'scroll',
                        'overflowX': 'scroll',
                        'width': '100%',
                        'minWidth': '100%',
                    },
                    css=[{'selector': '.row', 'rule': 'margin: 0'}]
                )
            ])
        ])
    ],width=10)
],no_gutters=True,style={"height":"100vh"})

def register_home_callbacks(app):

    @app.callback(
        Output('controls-container', 'style'),
        [Input('toggle', 'value')])

    def toggle_showmore_container(toggle_value):
        if toggle_value == 'Show More':
            return {'display': 'block','max-height':250,'overflow-y':'auto',"border-top":"1px black solid"}
        else:
            return {'display': 'none'}

    @app.callback(
        Output('controls-container2', 'style'),
        [Input('toggle2', 'value')])

    def toggle_showmore_container2(toggle_value):
        if toggle_value == 'Show More':
            return {'display': 'block','max-height':250,'overflow-y':'auto',"border-top":"1px black solid"}
        else:
            return {'display': 'none'}

    @app.callback(
        [Output('studies', 'value')],
        [Input('allstudies', 'n_clicks'),
        Input('dallstudies', 'n_clicks')],
        [State('studies', 'value'),
        State('studies', 'options')]
    )
    def select_deselect_all_studies(allstudies,dallstudies,studies_value,studies_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allstudies.n_clicks':
            return([[value['value'] for value in studies_options]])
        elif changed_id == 'dallstudies.n_clicks':
            return([[]])
        else:
            return([studies_value])

    @app.callback(
        [Output('studies2', 'value')],
        [Input('allstudies2', 'n_clicks'),
        Input('dallstudies2', 'n_clicks')],
        [State('studies2', 'value'),
        State('studies2', 'options')]
    )
    def select_deselect_all_studies2(allstudies,dallstudies,studies_value,studies_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allstudies2.n_clicks':
            return([[value['value'] for value in studies_options]])
        elif changed_id == 'dallstudies2.n_clicks':
            return([[]])
        else:
            return([studies_value])

    @app.callback(
        [Output('gasses', 'value')],
        [Input('allgas', 'n_clicks'),
        Input('dallgas', 'n_clicks')],
        [State('gasses', 'value'),
        State('gasses', 'options')]
    )
    def select_deselect_all_gasses(allgas,dallgas,gas_value,gas_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allgas.n_clicks':
            return([[value['value'] for value in gas_options]])
        elif changed_id == 'dallgas.n_clicks':
            return([[]])
        else:
            return([gas_value])

    @app.callback(
        [Output('gasses2', 'value')],
        [Input('allgas2', 'n_clicks'),
        Input('dallgas2', 'n_clicks')],
        [State('gasses2', 'value'),
        State('gasses2', 'options')]
    )
    def select_deselect_all_gasses2(allgas,dallgas,gas_value,gas_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allgas2.n_clicks':
            return([[value['value'] for value in gas_options]])
        elif changed_id == 'dallgas2.n_clicks':
            return([[]])
        else:
            return([gas_value])

    @app.callback(
        [Output('surfactants', 'value')],
        [Input('allsurf', 'n_clicks'),
        Input('dallsurf', 'n_clicks')],
        [State('surfactants', 'value'),
        State('surfactants', 'options')]
    )
    def select_deselect_all_surfactants(allsurf,dallsurf,surf_value,surf_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allsurf.n_clicks':
            return([[value['value'] for value in surf_options]])
        elif changed_id == 'dallsurf.n_clicks':
            return([[]])
        else:
            return([surf_value])

    @app.callback(
        [Output('surfactants2', 'value')],
        [Input('allsurf2', 'n_clicks'),
        Input('dallsurf2', 'n_clicks')],
        [State('surfactants2', 'value'),
        State('surfactants2', 'options')]
    )
    def select_deselect_all_surfactants2(allsurf,dallsurf,surf_value,surf_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allsurf2.n_clicks':
            return([[value['value'] for value in surf_options]])
        elif changed_id == 'dallsurf2.n_clicks':
            return([[]])
        else:
            return([surf_value])

    @app.callback(
        [Output('sconc', 'value')],
        [Input('allsconc', 'n_clicks'),
        Input('dallsconc', 'n_clicks')],
        [State('sconc', 'value'),
        State('sconc', 'options')]
    )
    def select_deselect_all_surfconc(allsconc,dallscon,sconc_value,sconc_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allsconc.n_clicks':
            return([[value['value'] for value in sconc_options]])
        elif changed_id == 'dallsconc.n_clicks':
            return([[]])
        else:
            return([sconc_value])

    @app.callback(
        [Output('sconc2', 'value')],
        [Input('allsconc2', 'n_clicks'),
        Input('dallsconc2', 'n_clicks')],
        [State('sconc2', 'value'),
        State('sconc2', 'options')]
    )
    def select_deselect_all_surfconc2(allsconc,dallscon,sconc_value,sconc_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allsconc2.n_clicks':
            return([[value['value'] for value in sconc_options]])
        elif changed_id == 'dallsconc2.n_clicks':
            return([[]])
        else:
            return([sconc_value])

    @app.callback(
        [Output('additives', 'value')],
        [Input('alladd', 'n_clicks'),
        Input('dalladd', 'n_clicks')],
        [State('additives', 'value'),
        State('additives', 'options')]
    )
    def select_deselect_all_additives(alladd,dalladd,add_value,add_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'alladd.n_clicks':
            return([[value['value'] for value in add_options]])
        elif changed_id == 'dalladd.n_clicks':
            return([[]])
        else:
            return([add_value])

    @app.callback(
        [Output('additives2', 'value')],
        [Input('alladd2', 'n_clicks'),
        Input('dalladd2', 'n_clicks')],
        [State('additives2', 'value'),
        State('additives2', 'options')]
    )
    def select_deselect_all_additives2(alladd,dalladd,add_value,add_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'alladd2.n_clicks':
            return([[value['value'] for value in add_options]])
        elif changed_id == 'dalladd2.n_clicks':
            return([[]])
        else:
            return([add_value])

    @app.callback(
        [Output('aconc', 'value')],
        [Input('allaconc', 'n_clicks'),
        Input('dallaconc', 'n_clicks')],
        [State('aconc', 'value'),
        State('aconc', 'options')]
    )
    def select_deselect_all_addconc(allaconc,dallaconc,aconc_value,aconc_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allaconc.n_clicks':
            return([[value['value'] for value in aconc_options]])
        elif changed_id == 'dallaconc.n_clicks':
            return([[]])
        else:
            return([aconc_value])

    @app.callback(
        [Output('aconc2', 'value')],
        [Input('allaconc2', 'n_clicks'),
        Input('dallaconc2', 'n_clicks')],
        [State('aconc2', 'value'),
        State('aconc2', 'options')]
    )
    def select_deselect_all_addconc2(allaconc,dallaconc,aconc_value,aconc_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'allaconc2.n_clicks':
            return([[value['value'] for value in aconc_options]])
        elif changed_id == 'dallaconc2.n_clicks':
            return([[]])
        else:
            return([aconc_value])

    @app.callback(
        [Output('lp', 'value')],
        [Input('alllp', 'n_clicks'),
        Input('dalllp', 'n_clicks')],
        [State('lp', 'value'),
        State('lp', 'options')]
    )
    def select_deselect_all_liquidphases(alllp,dalllp,lp_value,lp_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'alllp.n_clicks':
            return([[value['value'] for value in lp_options]])
        elif changed_id == 'dalllp.n_clicks':
            return([[]])
        else:
            return([lp_value])

    @app.callback(
        [Output('lp2', 'value')],
        [Input('alllp2', 'n_clicks'),
        Input('dalllp2', 'n_clicks')],
        [State('lp2', 'value'),
        State('lp2', 'options')]
    )
    def select_deselect_all_liquidphases2(alllp,dalllp,lp_value,lp_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'alllp2.n_clicks':
            return([[value['value'] for value in lp_options]])
        elif changed_id == 'dalllp2.n_clicks':
            return([[]])
        else:
            return([lp_value])

    @app.callback(
        [Output('compare_dropdown', 'style'),
        Output('compare_graph', 'style'),
        Output('compare_table', 'style'),
        Output('compare_graph_2D', 'style'),
        Output('compare_table_2D', 'style'),
        Output('toggle2', 'style')],
        [Input('addComp', 'value')])
    def toggle_compare_container(compare_value):
        if compare_value == 'Compare':
            return [{'display': 'block',"position":"absolute","top":"45%","margin-right":"auto","margin-left":"auto","width":"100%","text-align":"center"},
                    {'display': 'block'},
                    {'display': 'block'},
                    {'display': 'block'},
                    {'display': 'block'},
                    {"text-align":"center","margin":"auto","backgroundColor": 'white', "border-radius":3,"width":"80%"}]
        else:
            return [{'display': 'none'},
                    {'display': 'none'},
                    {'display': 'none'},
                    {'display': 'none'},
                    {'display': 'none'},
                    {'display': 'none'}]

    @app.callback(
        Output('table', 'style_data_conditional'),
        [Input("select-xaxis", "value"),
        Input("select-yaxis", "value"),
        Input("select-zaxis", "value")]
    )
    def update_master_table_styles(x,y,z):
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
        [Output("comp1_3D_graph", "figure"),
        Output("comp1_3D_table", "data"),
        Output("comp1_3D_table", "columns")],
        [Input("select-xaxis", "value"),
        Input("select-yaxis", "value"),
        Input("select-zaxis", "value"),
        Input('addComp', 'value'),
        Input('normalize', 'value'),
        Input("bestfit", "value"),
        Input("input_fit", "value"),
        Input('studies', 'value'),
        Input('gasses', 'value'),
        Input('surfactants', 'value'),
        Input('sconc', 'value'),
        Input('additives', 'value'),
        Input('aconc', 'value'),
        Input('lp', 'value')],
    )
    def update_comp1_3D_graph(selected_x, selected_y, selected_z, comp, normalize, fit, order, stu, ga, sur, surc, add, addc, lp):
        c = dv[dv['Study'].isin(stu)]
        l = c[c['Gas'].isin(ga)]
        ea = l[l['Surfactant'].isin(sur)]
        n = ea[ea["Surfactant Concentration"].isin(surc)]
        e = n[n['Additive'].isin(add)]
        d = e[e['Additive Concentration'].isin(addc)]
        cleaned = d[d['LiquidPhase'].isin(lp)]

        cleaned = cleaned.dropna(subset=[selected_x, selected_y, selected_z],axis="rows")
        cleaned.reset_index(drop=True)
        cleaned.sort_values(by=selected_x, inplace=True)

        data = []

        for i in unique_studies:
            name_array = cleaned[cleaned.Study == i]

            if len(name_array[selected_x]) > 2:
                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
                z = np.array(name_array[selected_z])
                if "Normalize X" in normalize:
                    if max(x) == min(x):
                        x = np.full_like(x, 0.5)
                    else:
                        x = (x-min(x))/(max(x)-min(x))
                    x[x == 0] = 0.001

                if "Normalize Y" in normalize:
                    if max(y) == min(y):
                        y = np.full_like(y, 0.5)
                    else:
                        y = (y-min(y))/(max(y)-min(y))
                    y[y == 0] = 0.001

                if "Normalize Z" in normalize:
                    if max(z) == min(z):
                        z = np.full_like(z, 0.5)
                    else:
                        z = (z-min(z))/(max(z)-min(z))
                    z[z == 0] = 0.001
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scatter3d(x = x, y = y, z = z,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='lines+markers', line={'color' : name_array.Color.values[0]},
                    marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scatter3d(x = x, y = y, z = z,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                data.append(trace)

            elif('Line' in fit):
                trace = go.Scatter3d(x = x, y = y, z = z,
                hovertemplate= "Gas: " + name_array.Gas
                + "<br />Surfactant: " + name_array.Surfactant
                + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                + "<br />Additive: " + name_array.Additive
                + "<br />Concentration Additive: " + name_array['Additive Concentration']
                + "<br />Liquid Phase: " + name_array.LiquidPhase,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

                data.append(trace)

            colorscale= [[0, name_array.Color.values[0]], [1, name_array.Color.values[0]]]
            if('Poly-Fit' in fit):
                if('Scatter' in fit):
                    showLegend = False
                else:
                    showLegend = True

                d = np.c_[x,y,z]

                # regular grid covering the domain of the data
                mn = np.min(d, axis=0)
                mx = np.max(d, axis=0)
                X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
                XX = X.flatten()
                YY = Y.flatten()

                if order == 1:
                    # Poly-Fit linear plane
                    A = np.c_[d[:,0], d[:,1], np.ones(d.shape[0])]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])    # coefficients

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    # evaluate it on grid
                    # Z = C[0]*X + C[1]*Y + C[2]

                    equation = "z = {a}x + {b}y + {c}".format(a=f_new[0], b=f_new[1], c=f_new[2])

                    # or expressed using matrix/vector product
                    Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

                elif order == 2:
                    # Poly-Fit quadratic curve
                    # M = [ones(size(x)), x, y, x.*y, x.^2 y.^2]
                    A = np.c_[np.ones(d.shape[0]), d[:,:2], np.prod(d[:,:2], axis=1), d[:,:2]**2]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    equation = "z = {a}x² + {b}y² + {c}xy + {d}x + {e}y + {f}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3],e=f_new[4],f=f_new[5])

                    # evaluate it on a grid
                    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)

                elif order == 3:
                    # M = [ones(size(x)), x, y, x.^2, x.*y, y.^2, x.^3, x.^2.*y, x.*y.^2, y.^3]
                    A = np.c_[np.ones(d.shape[0]), d[:,:2], d[:,0]**2, np.prod(d[:,:2], axis=1), \
                            d[:,1]**2, d[:,0]**3, np.prod(np.c_[d[:,0]**2,d[:,1]],axis=1), \
                            np.prod(np.c_[d[:,0],d[:,1]**2],axis=1), d[:,2]**3]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    equation = "z = {a}x³ + {b}y³ + {c}x²y + {d}xy² + {e}x² + {f}y² + {g}xy + {h}x + {i}y + {j}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3],e=f_new[4],f=f_new[5],g=f_new[6],h=f_new[7],i=f_new[8],j=f_new[9])

                    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX**2, XX*YY, YY**2, XX**3, XX**2*YY, XX*YY**2, YY**3], C).reshape(X.shape)

                trace = go.Surface(x = X, y = Y, z = Z,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= equation,
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Log-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def logarithmic(data, a, b, c, d):
                    x = data[0]
                    y = data[1]
                    return  a * np.log(b * x) * np.log(c * y) + d

                popt, _ = curve_fit(logarithmic, [x, y], z, maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = logarithmic(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * log({b} * x) * log({c} * y) + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Exp-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def exponential(data, a, b, c, d):
                    x = data[0]
                    y = data[1]
                    return a * np.exp(-b * x) * np.exp(-c * y) + d

                popt, _ = curve_fit(exponential, [x, y], z, p0=(1, 1e-6, 1e-6, 1), maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = exponential(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * e<sup>({b} * x)</sup> * e<sup>({c} * y)</sup> + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Power-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def power(data, a, M, N, b):
                    x = data[0]
                    y = data[1]
                    return a * np.power(x,M) * np.power(y,N) + b

                popt, _ = curve_fit(power, [x, y], z, maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = power(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * x<sup>{M}</sup> * y<sup>{N}</sup> + {d}".format(a=f_new[0],M=f_new[1],N=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

        cleaned = cleaned[[selected_x,selected_y, selected_z]]

        if(comp == "No Compare"):
            legend_orientation={
                    "font_size": 24,
            }

        if(comp == "Compare"):
            legend_orientation={
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "valign":"middle",
                    "font_size": 20,
            }

        return [
            {"data": data,
            "layout": go.Layout(
                hovermode="closest",
                legend=legend_orientation,
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
                    "b":0,
                    "l":0,
                    "r":0
                },
                height=Graph_Height
            )},
            
            cleaned.to_dict('records'), 
            [{'id': c, 'name': c} for c in cleaned.columns]
        ]

    @app.callback(
        [Output("comp2_3D_graph", "figure"),
        Output("comp2_3D_table", "data"),
        Output("comp2_3D_table", "columns")],
        [Input("select-xaxis2", "value"),
        Input("select-yaxis2", "value"),
        Input("select-zaxis2", "value"),
        Input("addComp","value"),
        Input("normalize2","value"),
        Input("bestfit2", "value"),
        Input("input_fit2", "value"),
        Input('studies2', 'value'),
        Input('gasses2', 'value'),
        Input('surfactants2', 'value'),
        Input('sconc2', 'value'),
        Input('additives2', 'value'),
        Input('aconc2', 'value'),
        Input('lp2', 'value')],
    )
    def update_comp2_3D_graph(selected_x, selected_y, selected_z, comp, normalize, fit, order, stu, ga, sur, surc, add, addc, lp):
        if comp == "No Compare":
            return [{},[],[]]

        c = dv[dv['Study'].isin(stu)]
        l = c[c['Gas'].isin(ga)]
        ea = l[l['Surfactant'].isin(sur)]
        n = ea[ea["Surfactant Concentration"].isin(surc)]
        e = n[n['Additive'].isin(add)]
        d = e[e['Additive Concentration'].isin(addc)]
        cleaned = d[d['LiquidPhase'].isin(lp)]

        cleaned = cleaned.dropna(subset=[selected_x, selected_y, selected_z],axis="rows")
        cleaned.reset_index(drop=True)
        cleaned.sort_values(by=selected_x, inplace=True)

        data = []

        for i in unique_studies:
            name_array = cleaned[cleaned.Study == i]

            if len(name_array[selected_x]) > 2:
                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
                z = np.array(name_array[selected_z])
                if "Normalize X" in normalize:
                    if max(x) == min(x):
                        x = np.full_like(x, 0.5)
                    else:
                        x = (x-min(x))/(max(x)-min(x))
                    x[x == 0] = 0.001

                if "Normalize Y" in normalize:
                    if max(y) == min(y):
                        y = np.full_like(y, 0.5)
                    else:
                        y = (y-min(y))/(max(y)-min(y))
                    y[y == 0] = 0.001

                if "Normalize Z" in normalize:
                    if max(z) == min(z):
                        z = np.full_like(z, 0.5)
                    else:
                        z = (z-min(z))/(max(z)-min(z))
                    z[z == 0] = 0.001
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scatter3d(x = x, y = y, z = z,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='lines+markers', line={'color' : name_array.Color.values[0]},
                    marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scatter3d(x = x, y = y, z = z,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                data.append(trace)

            elif('Line' in fit):
                trace = go.Scatter3d(x = x, y = y, z = z,
                hovertemplate= "Gas: " + name_array.Gas
                + "<br />Surfactant: " + name_array.Surfactant
                + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                + "<br />Additive: " + name_array.Additive
                + "<br />Concentration Additive: " + name_array['Additive Concentration']
                + "<br />Liquid Phase: " + name_array.LiquidPhase,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

                data.append(trace)

            colorscale= [[0, name_array.Color.values[0]], [1, name_array.Color.values[0]]]

            if('Poly-Fit' in fit):
                if('Scatter' in fit):
                    showLegend = False
                else:
                    showLegend = True

                d = np.c_[x,y,z]

                # regular grid covering the domain of the data
                mn = np.min(d, axis=0)
                mx = np.max(d, axis=0)
                X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
                XX = X.flatten()
                YY = Y.flatten()

                if order == 1:
                    # Poly-Fit linear plane
                    A = np.c_[d[:,0], d[:,1], np.ones(d.shape[0])]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])    # coefficients

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    # evaluate it on grid
                    # Z = C[0]*X + C[1]*Y + C[2]

                    equation = "z = {a}x + {b}y + {c}".format(a=f_new[0], b=f_new[1], c=f_new[2])

                    # or expressed using matrix/vector product
                    Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

                elif order == 2:
                    # Poly-Fit quadratic curve
                    # M = [ones(size(x)), x, y, x.*y, x.^2 y.^2]
                    A = np.c_[np.ones(d.shape[0]), d[:,:2], np.prod(d[:,:2], axis=1), d[:,:2]**2]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    equation = "z = {a}x² + {b}y² + {c}xy + {d}x + {e}y + {f}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3],e=f_new[4],f=f_new[5])

                    # evaluate it on a grid
                    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)

                elif order == 3:
                    # M = [ones(size(x)), x, y, x.^2, x.*y, y.^2, x.^3, x.^2.*y, x.*y.^2, y.^3]
                    A = np.c_[np.ones(d.shape[0]), d[:,:2], d[:,0]**2, np.prod(d[:,:2], axis=1), \
                            d[:,1]**2, d[:,0]**3, np.prod(np.c_[d[:,0]**2,d[:,1]],axis=1), \
                            np.prod(np.c_[d[:,0],d[:,1]**2],axis=1), d[:,2]**3]
                    C,_,_,_ = np.linalg.lstsq(A, d[:,2])

                    f_new = []
                    for num in C:
                        if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                            f_new.append(format(num,'.3e'))
                        else:
                            f_new.append(np.round(num,3))

                    equation = "z = {a}x³ + {b}y³ + {c}x²y + {d}xy² + {e}x² + {f}y² + {g}xy + {h}x + {i}y + {j}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3],e=f_new[4],f=f_new[5],g=f_new[6],h=f_new[7],i=f_new[8],j=f_new[9])

                    Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX**2, XX*YY, YY**2, XX**3, XX**2*YY, XX*YY**2, YY**3], C).reshape(X.shape)

                trace = go.Surface(x = X, y = Y, z = Z,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= equation,
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Log-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def logarithmic(data, a, b, c, d):
                    x = data[0]
                    y = data[1]
                    return  a * np.log(b * x) * np.log(c * y) + d

                popt, _ = curve_fit(logarithmic, [x, y], z, maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = logarithmic(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * log({b} * x) * log({c} * y) + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Exp-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def exponential(data, a, b, c, d):
                    x = data[0]
                    y = data[1]
                    return a * np.exp(-b * x) * np.exp(-c * y) + d

                popt, _ = curve_fit(exponential, [x, y], z, p0=(1, 1e-6, 1e-6, 1), maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = exponential(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * e<sup>({b} * x)</sup> * e<sup>({c} * y)</sup> + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Power-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def power(data, a, M, N, b):
                    x = data[0]
                    y = data[1]
                    return a * np.power(x,M) * np.power(y,N) + b

                popt, _ = curve_fit(power, [x, y], z, maxfev = 999999999)

                # create surface function model
                # setup data points for calculating surface model
                X = np.linspace(min(x), max(x), 20)
                Y = np.linspace(min(y), max(y), 20)

                # create coordinate arrays for vectorized evaluations
                x_new, y_new = np.meshgrid(X, Y)

                # calculate Z coordinate array
                z_new = power(np.array([x_new, y_new]), *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Surface(x = x_new, y = y_new, z = z_new,
                colorscale=colorscale, opacity=0.75,
                hovertemplate= "y = {a} * x<sup>{M}</sup> * y<sup>{N}</sup> + {d}".format(a=f_new[0],M=f_new[1],N=f_new[2],d=f_new[3]),
                name=i,showscale=False,showlegend=showLegend,legendgroup=i)

                data.append(trace)

        cleaned = cleaned[[selected_x,selected_y, selected_z]]

        return [
            {"data": data,
            "layout": go.Layout(
                hovermode="closest",
                legend={
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "valign":"middle",
                    "font_size": 20,
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
                    "b":0,
                    "l":0,
                    "r":0
                },
                height=Graph_Height
            )},
            
            cleaned.to_dict('records'), 
            [{'id': c, 'name': c} for c in cleaned.columns]
        ]

    @app.callback(
        [Output("comp1_2D_graph", "figure"),
        Output("comp1_2D_table", "data"),
        Output("comp1_2D_table", "columns")],
        [Input("select-xaxis", "value"),
        Input("select-yaxis", "value"),
        Input('addComp', 'value'),
        Input('normalize', 'value'),
        Input("bestfit", "value"),
        Input("input_fit", "value"),
        Input('studies', 'value'),
        Input('gasses', 'value'),
        Input('surfactants', 'value'),
        Input('sconc', 'value'),
        Input('additives', 'value'),
        Input('aconc', 'value'),
        Input('lp', 'value')],
    )
    def update_comp1_2D_graph(selected_x, selected_y, comp, normalize, fit, order, stu, ga, sur, surc, add, addc, lp):
        c = dv[dv['Study'].isin(stu)]
        l = c[c['Gas'].isin(ga)]
        ea = l[l['Surfactant'].isin(sur)]
        n = ea[ea["Surfactant Concentration"].isin(surc)]
        e = n[n['Additive'].isin(add)]
        d = e[e['Additive Concentration'].isin(addc)]
        cleaned = d[d['LiquidPhase'].isin(lp)]

        cleaned = cleaned.dropna(subset=[selected_x, selected_y],axis="rows")
        cleaned.reset_index(drop=True)
        cleaned.sort_values(by=selected_x, inplace=True)

        data = []

        for i in unique_studies:
            name_array = cleaned[cleaned.Study == i]

            if len(name_array[selected_x]) > 2:
                if('Average Y-axis' in normalize):
                    cats = np.unique(name_array[selected_x].values)
                    for j in cats:
                        rows_cat = name_array[name_array[selected_x] == j]
                        first_row = rows_cat.iloc[[0],:]

                        if len(list(dict.fromkeys((rows_cat["Gas"].values)))) > 1:
                            first_row["Gas"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Surfactant"].values)))) > 1:
                            first_row["Surfactant"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Surfactant Concentration"].values)))) > 1:
                            first_row["Surfactant Concentration"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Additive"].values)))) > 1:
                            first_row["Additive"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Additive Concentration"].values)))) > 1:
                            first_row["Additive Concentration"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["LiquidPhase"].values)))) > 1:
                            first_row["LiquidPhase"] = "Refine Further"

                        avg = rows_cat[selected_y].mean()
                        first_row[selected_y] = avg

                        name_array = name_array[name_array[selected_x] != j]
                        name_array = name_array.append(first_row,ignore_index=True)

                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
                if "Normalize X" in normalize:
                    if max(x) == min(x):
                        x = np.full_like(x, 0.5)
                    else:
                        x = (x-min(x))/(max(x)-min(x))
                    x[x == 0] = 0.001

                if "Normalize Y" in normalize:
                    if max(y) == min(y):
                        y = np.full_like(y, 0.5)
                    else:
                        y = (y-min(y))/(max(y)-min(y))
                    y[y == 0] = 0.001
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scattergl(x = x, y = y,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='lines+markers', line={'color' : name_array.Color.values[0]},
                    marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scattergl(x = x, y = y,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                data.append(trace)

            elif('Line' in fit):
                trace = go.Scattergl(x = x, y = y,
                hovertemplate= "Gas: " + name_array.Gas
                + "<br />Surfactant: " + name_array.Surfactant
                + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                + "<br />Additive: " + name_array.Additive
                + "<br />Concentration Additive: " + name_array['Additive Concentration']
                + "<br />Liquid Phase: " + name_array.LiquidPhase,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

                data.append(trace)

            if('Poly-Fit' in fit):
                if('Scatter' in fit):
                    showLegend = False
                else:
                    showLegend = True

                z = np.polyfit(x,y,order)
                f = np.poly1d(z)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_res = f(x)
                y_new = f(x_new)

                f_new = []
                for num in f:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                if order == 1:
                    equation = "y = {a}x + {b}".format(a=f_new[0],b=f_new[1])
                    residuals = y- y_res
                    ss_res = np.sum(residuals**2)
                    ss_tot = np.sum((y-np.mean(y))**2)
                    r_squared = str(np.round(1 - (ss_res / ss_tot),3))

                elif order == 2:
                    equation = "y = {a}x² + {b}x + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2])
                    r_squared = "Non-Linear"
                elif order == 3:
                    equation = "y = {a}x³ + {b}x² + {c}x + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3])
                    r_squared = "Non-Linear"

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= equation
                + "<br />R Squared: " + r_squared,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Log-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def logarithmic(x, a, b, c):
                    return  a * np.log(b * x) + c

                popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = logarithmic(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * log({b} * x) + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Exp-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def exponential(x, a, b, c):
                    return a * np.exp(-b * x) + c

                popt, _ = curve_fit(exponential, x, y, p0=(1, 1e-6, 1), maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = exponential(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * e<sup>({b} * x)</sup> + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Power-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def power(x, a, N, b):
                    return a * np.power(x,N) + b

                popt, _ = curve_fit(power, x, y, maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = power(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * x<sup>{N}</sup> + {c}".format(a=f_new[0],N=f_new[1],c=f_new[2]),
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

        if(comp == "No Compare"):
            legend_orientation={
                    "font_size": 24,
            }

        if(comp == "Compare"):
            legend_orientation={
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "font_size": 20,
            }

        cleaned = cleaned[[selected_x,selected_y]]

        return [
            {'data': data,
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
                legend=legend_orientation,
                font={
                    "family":"Times New Roman",
                },
                hovermode="closest",
                height=Graph_Height
            )},
        
            cleaned.to_dict('records'), 
            [{'id': c, 'name': c} for c in cleaned.columns]
        ]

    @app.callback(
        [Output("comp2_2D_graph", "figure"),
        Output("comp2_2D_table", "data"),
        Output("comp2_2D_table", "columns")],
        [Input("select-xaxis2", "value"),
        Input("select-yaxis2", "value"),
        Input('addComp', 'value'),
        Input('normalize2', 'value'),
        Input("bestfit2", "value"),
        Input("input_fit2", "value"),
        Input('studies2', 'value'),
        Input('gasses2', 'value'),
        Input('surfactants2', 'value'),
        Input('sconc2', 'value'),
        Input('additives2', 'value'),
        Input('aconc2', 'value'),
        Input('lp2', 'value')],
    )
    def update_comp2_2D_graph(selected_x, selected_y, comp, normalize, fit, order, stu, ga, sur, surc, add, addc, lp):
        if comp == "No Compare":
            return [{},[],[]]

        c = dv[dv['Study'].isin(stu)]
        l = c[c['Gas'].isin(ga)]
        ea = l[l['Surfactant'].isin(sur)]
        n = ea[ea["Surfactant Concentration"].isin(surc)]
        e = n[n['Additive'].isin(add)]
        d = e[e['Additive Concentration'].isin(addc)]
        cleaned = d[d['LiquidPhase'].isin(lp)]

        cleaned = cleaned.dropna(subset=[selected_x, selected_y],axis="rows")
        cleaned.reset_index(drop=True)
        cleaned.sort_values(by=selected_x, inplace=True)

        data = []

        for i in unique_studies:
            name_array = cleaned[cleaned.Study == i]

            if len(name_array[selected_x]) > 2:
                if('Average Y-axis' in normalize):
                    cats = np.unique(name_array[selected_x].values)
                    for j in cats:
                        rows_cat = name_array[name_array[selected_x] == j]
                        first_row = rows_cat.iloc[[0],:]

                        if len(list(dict.fromkeys((rows_cat["Gas"].values)))) > 1:
                            first_row["Gas"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Surfactant"].values)))) > 1:
                            first_row["Surfactant"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Surfactant Concentration"].values)))) > 1:
                            first_row["Surfactant Concentration"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Additive"].values)))) > 1:
                            first_row["Additive"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["Additive Concentration"].values)))) > 1:
                            first_row["Additive Concentration"] = "Refine Further"

                        if len(list(dict.fromkeys((rows_cat["LiquidPhase"].values)))) > 1:
                            first_row["LiquidPhase"] = "Refine Further"

                        avg = rows_cat[selected_y].mean()
                        first_row[selected_y] = avg

                        name_array = name_array[name_array[selected_x] != j]
                        name_array = name_array.append(first_row,ignore_index=True)

                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
                if "Normalize X" in normalize:
                    if max(x) == min(x):
                        x = np.full_like(x, 0.5)
                    else:
                        x = (x-min(x))/(max(x)-min(x))
                    x[x == 0] = 0.001

                if "Normalize Y" in normalize:
                    if max(y) == min(y):
                        y = np.full_like(y, 0.5)
                    else:
                        y = (y-min(y))/(max(y)-min(y))
                    y[y == 0] = 0.001
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scattergl(x = x, y = y,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='lines+markers', line={'color' : name_array.Color.values[0]},
                    marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scattergl(x = x, y = y,
                    hovertemplate= "Gas: " + name_array.Gas
                    + "<br />Surfactant: " + name_array.Surfactant
                    + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                    + "<br />Additive: " + name_array.Additive
                    + "<br />Concentration Additive: " + name_array['Additive Concentration']
                    + "<br />Liquid Phase: " + name_array.LiquidPhase,
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                data.append(trace)

            elif('Line' in fit):
                trace = go.Scattergl(x = x, y = y,
                hovertemplate= "Gas: " + name_array.Gas
                + "<br />Surfactant: " + name_array.Surfactant
                + "<br />Concentration Surfactant: " + name_array["Surfactant Concentration"]
                + "<br />Additive: " + name_array.Additive
                + "<br />Concentration Additive: " + name_array['Additive Concentration']
                + "<br />Liquid Phase: " + name_array.LiquidPhase,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

                data.append(trace)

            if('Poly-Fit' in fit):
                if('Scatter' in fit):
                    showLegend = False
                else:
                    showLegend = True

                z = np.polyfit(x,y,order)
                f = np.poly1d(z)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_res = f(x)
                y_new = f(x_new)

                f_new = []
                for num in f:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                if order == 1:
                    equation = "y = {a}x + {b}".format(a=f_new[0],b=f_new[1])
                    residuals = y- y_res
                    ss_res = np.sum(residuals**2)
                    ss_tot = np.sum((y-np.mean(y))**2)
                    r_squared = str(np.round(1 - (ss_res / ss_tot),3))

                elif order == 2:
                    equation = "y = {a}x² + {b}x + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2])
                    r_squared = "Non-Linear"
                elif order == 3:
                    equation = "y = {a}x³ + {b}x² + {c}x + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3])
                    r_squared = "Non-Linear"

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= equation
                + "<br />R Squared: " + r_squared,
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Log-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def logarithmic(x, a, b, c):
                    return  a * np.log(b * x) + c

                popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = logarithmic(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * log({b} * x) + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Exp-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def exponential(x, a, b, c):
                    return a * np.exp(-b * x) + c

                popt, _ = curve_fit(exponential, x, y, p0=(1, 1e-6, 1), maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = exponential(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * e<sup>({b} * x)</sup> + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

            if('Power-Fit' in fit):
                if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                    showLegend = False
                else:
                    showLegend = True

                def power(x, a, N, b):
                    return a * np.power(x,N) + b

                popt, _ = curve_fit(power, x, y, maxfev = 999999999)

                x_new = np.linspace(x[0], x[-1], 1000)
                y_new = power(x_new, *popt)

                f_new = []
                for num in popt:
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertemplate= "y = {a} * x<sup>{N}</sup> + {c}".format(a=f_new[0],N=f_new[1],c=f_new[2]),
                hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,showlegend=showLegend,legendgroup=i)

                data.append(trace)

        cleaned = cleaned[[selected_x,selected_y]]

        return [
            {'data': data,
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
                    "orientation":"h",
                    "xanchor":"center",
                    "x":0.5,
                    "yanchor":"bottom",
                    "y":1,
                    "valign":"middle",
                    "font_size": 20,
                },
                font={
                    "family":"Times New Roman",
                },
                hovermode="closest",
                height=Graph_Height
            )},
        
            cleaned.to_dict('records'), 
            [{'id': c, 'name': c} for c in cleaned.columns]
        ]

def Home():
    return home