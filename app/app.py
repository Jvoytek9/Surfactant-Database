import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from home import Home, register_home_callbacks
from about import About, register_about_callbacks

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {
                        'name' : 'author',
                        'content' : 'Josh Voytek'
                    },
                    {
                        'name' : 'type',
                        'property' : 'og:type',
                        'content' : 'Data Visualization'
                    },
                    {
                        'name' : 'description',
                        'property' : 'og:description',
                        'content' : 'Compilation of modern Surfactant/Foam Literature for applications in waterless geothermal fracking. ' +
                        'Built with the concept of being added to easily.'
                    },
                    {
                        'name' : 'image',
                        'property' : 'og:image',
                        'content' : 'assets/thumbnail.PNG'
                    },
                    {
                        'name' : 'keywords',
                        'property' : 'og:keywords',
                        'content' : 'Python, Plotly, Dash, Waterless, Geothermal, Fracking'
                    }
                ]
            )

register_home_callbacks(app)
register_about_callbacks(app)

server = app.server
app.title = "Foam Literature"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/about':
        return About()
    else:
        return Home()

if __name__ == '__main__':
    app.run_server(debug=False)