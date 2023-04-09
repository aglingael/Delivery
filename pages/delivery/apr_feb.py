import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask_babel import get_locale, gettext

from graphs.apr_feb import postal_aggr_increase, hist_feb_apr, postal_dot_plot, postal_apr_feb, ratio_nadr_apr_feb, \
    apr_parcels_dist, ratio_nvisits_apr_feb
from pages.sources import display_source_providers, source_delivery


def display_apr_feb():
    return [
        html.H2(gettext("Increase of parcels delivered in April compared to February")),
        html.P([(
            'Private comment'),
            html.Br(),
            ('Private comment')],
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='monthly-increase-postal-code-aggr', figure=postal_aggr_increase(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(
            gettext("Comparison of parcels delivered by address and by business day in April compared to February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='monthly-increase-postal-code-aggr', figure=postal_dot_plot(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='monthly-increase-postal-code-aggr', figure=postal_apr_feb(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Number of visits per address in April compared to February")),
        html.P([(
            'Private comment'),
            html.Br(),
            (
                'Private comment')],
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='hist_feb_apr', figure=hist_feb_apr(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Ratio of addresses number of April over February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='ratio_nadr_apr_feb', figure=ratio_nadr_apr_feb(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Ratio of visits number of April over February")),
        html.P((
            'Private comment'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='ratio_nvisits_apr_feb', figure=ratio_nvisits_apr_feb(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        html.Br(),
        html.H2(gettext("Distribution of parcels numbers in April")),
        html.P((
            'Private comment'
            'delivery'),
            style={'text-align': 'justify'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='apr_parcels_dist', figure=apr_parcels_dist(),
                              config=dict(locale=str(get_locale()))), className="col-12"),
        ]),
        display_source_providers(source_delivery)
    ]
