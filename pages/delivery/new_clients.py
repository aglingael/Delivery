import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.new_clients import new_clients_weeks_percent_address, new_clients_weeks_percent_visits, cum_clients_weeks_address, ex_clients_weeks_address, norm_new_clients_dist
from pages.sources import display_source_providers, source_delivery


def display_new_clients():
    return [
        html.H2(gettext("Percentage of new/old clients in weeks after February")),
        html.P((
            'Private comment'
        ), style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='new_clients_weeks_percent_address', figure=new_clients_weeks_percent_address(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Percentage of visits of new/old clients in weeks after February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='new_clients_weeks_percent_visits', figure=new_clients_weeks_percent_visits(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Cumulative number of new/old clients visited in weeks after February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='cum_clients_weeks_address', figure=cum_clients_weeks_address(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Exclusive number of new/old clients visited in weeks after February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='ex_clients_weeks_address', figure=ex_clients_weeks_address(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext(
            "Distribution of addresses not visited in February but in the following weeks")),
        html.P((
            'Private comment'
            ),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='norm_new_clients_dist', figure=norm_new_clients_dist(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_delivery)
    ]
