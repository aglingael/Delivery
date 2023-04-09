import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.volumes import daily_volume, weekly_visits_per_address_map
from pages.sources import display_source_providers, source_delivery


def display_volumes():
    nc_page = [
        html.H2(gettext("Daily number of visits (week days)")),
        html.P(('Private comment'),
               style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='total-daily-volumes', figure=daily_volume(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Number of visits per address every week")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='total-volume-postal-code', figure=weekly_visits_per_address_map(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_delivery)
    ]
    return nc_page
