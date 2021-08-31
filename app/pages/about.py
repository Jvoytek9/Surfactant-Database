from app import app

from datetime import date
from cv2 import cv2
import base64
import tempfile
import numpy as np
import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

today = date.today()
today = today.strftime("%m/%d/%Y")

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Link('Home', href='/',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18,'width':'20%'})),
        dbc.Col([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Bubble Analyzer', children=[
                    html.Div([
                            dcc.Graph(id="output-data-upload",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': 'Image_Graph'}
                            })
                        ]),

                    html.Div(
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                html.P('Drag and Drop or Select Video(10 mb Limit)',style={"display":"inline"})
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px',
                                'cursor': 'pointer'
                            },
                            multiple=False,
                            max_size = 10000000,
                            accept = "video/*"
                        ),
                    id="upload-container"),

                    html.Div(
                        dbc.Button('Continue', id='continue', n_clicks=0,size="lg",outline=True,color="dark",style={"display":"None"})
                    ,style={"margin":"auto","position":"absolute","right":10,"bottom":10})
                ]),
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
        ],style={"backgroundColor":"white"},width=8),
        dbc.Col(style={'backgroundColor': '#9E1B34',"height":"100vh",'width':'20%'})
    ],style={'backgroundColor': '#9E1B34',"height":"100%"},no_gutters=True)
])

@app.callback([Output('output-data-upload', 'figure'),
            Output('continue', 'style'),
            Output('upload-container', 'style')],
            [Input('upload-data', 'contents'),
            Input('continue', 'n_clicks')])
def update_output(list_of_contents,conbut):
    if list_of_contents is not None:
        list_of_contents = list_of_contents.split(",")
        list_of_contents = list_of_contents[1].strip()
        if len(list_of_contents) % 4:
            list_of_contents += '=' * (4 - len(list_of_contents) % 4)

        temp_path = tempfile.gettempdir()
        decoded_string = base64.b64decode(list_of_contents)

        with open(temp_path+'/video.mp4', 'wb') as wfile:
            wfile.write(decoded_string)

        vidObj = cv2.VideoCapture(temp_path+'/video.mp4')

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        final_data= []
        data = []
        data2 = []
        iteration = 0
        success = True
        tracked = False
        multiTracker = cv2.MultiTracker_create()

        def Find_Circles(img):
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.bilateralFilter(gray, 7, 50, 50)
            circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 70, param1=110, param2=10, minRadius=20, maxRadius=100)

            return circles

        def Draw_and_Track_Circles(img,circles,tracked,count,iteration):
            if circles is not None:
                circles = np.int16(np.around(circles))

                if tracked is False:
                    for i in circles[0, :]:
                        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0),2)
                        cv2.putText(img,str(count),(i[0], i[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                        box = (i[0], i[1], 2*i[2], 2*i[2])
                        multiTracker.add(cv2.TrackerCSRT_create(), img, box)
                        final_data.append([count,iteration,i[0]/100,i[1]/100,(np.pi*i[2]**2)/(100**2)])
                        count += 1

                else:
                    (_, circles) = multiTracker.update(img)
                    circles = np.int16(np.around(circles))
                    for circle in circles:
                        radius = int(circle[2]/2)

                        cv2.circle(img, (circle[0], circle[1]), radius, (0, 255, 0),2)
                        cv2.putText(img,str(count),(circle[0], circle[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

                        final_data.append([count,iteration,circle[0]/100,circle[1]/100,(np.pi * radius**2)/(100**2)])

                        count += 1

                return(None)

            else:
                return(final_data)

        if changed_id == 'continue.n_clicks':

            while success:
                iteration += 1
                success, img = vidObj.read()

                if img is not None:
                    _ = Draw_and_Track_Circles(img, Find_Circles(img),tracked,1,iteration)
                    tracked = True

                else:
                    success = False
                    final_data = Draw_and_Track_Circles(np.array([]), None,tracked,0,iteration)
                    df = pd.DataFrame(final_data, columns =['Number', 'Iterations', 'X', 'Y', 'Area'])

                    numbers = sorted(list(dict.fromkeys(df['Number'])))

                    for i in numbers:
                        num_array = df[df.Number == i]
                        trace = go.Scattergl(x = num_array['Iterations'], y = num_array['Area'],name="Bubble " + str(i))
                        data2.append(trace)

                    return[
                    {
                        'data': data2,
                        'layout': go.Layout(
                            yaxis={
                                "title":"Area(mm²)",
                                "titlefont_size":20,
                                "tickfont_size":18,
                            },
                            xaxis={
                                "title":"Iterations(frames)",
                                "titlefont_size":20,
                                "tickfont_size":18
                            },
                            font={
                                "family":"Times New Roman",
                            },
                            hovermode="closest",
                            height=610
                        ),
                    },
                    {"display":"None"},
                    {"display":"block"}]

        else:
            _, img = vidObj.read()
            _ = Draw_and_Track_Circles(img, Find_Circles(img),False,1,1)
            trace = go.Image(z=img)
            data.append(trace)
            return(
                {
                    'data': data,
                    'layout': go.Layout(
                        yaxis={
                            "title":"Y Position(mm)",
                            "titlefont_size":20,
                            "tickfont_size":18
                        },
                        xaxis={
                            "title":"X Position(mm)",
                            "titlefont_size":20,
                            "tickfont_size":18
                        },
                        font={
                            "family":"Times New Roman",
                        },
                        hovermode="closest",
                        height=610
                    ),
                },
                {"display":"block"},
                {"display":"None"},)

    else:
        return[
        {
            'data': [],
            'layout': go.Layout(
                height=610
            )
        },
        {"display":"None"},
        {"display":"block"}]