import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.success import daily_success, success_map_week_year_slider, success_by_hour_and_week_slider, success_volume_by_postal_slider
from pages.sources import display_source_providers, source_delivery


def display_success():
    return [
        html.H2(gettext("Daily delivery success rate (week days)")),
        html.P(('Private comment'),
                style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='total-daily-success', figure=daily_success(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Success rate over the weeks")),
        html.P(('Private comment'),
                style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='weekly-year-success-rate-postal-code', figure=success_map_week_year_slider(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Success rate per hour over the weeks")),
        html.P(('Private comment'),
                style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='weekly-success-rate-hour', figure=success_by_hour_and_week_slider(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Success rate and volume per postal over the weeks")),
        html.P([('Private comment'),
                html.Br(),
                ('Private comment')],
                style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='weekly-success-volume-postal', figure=success_volume_by_postal_slider(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_delivery)
    ]
