from app import app
from app import server
from pages import home, about

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        return about.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)