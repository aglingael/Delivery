import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_babel import get_locale, gettext, lazy_gettext

from pages import AppMenu, AppLink, get_translation


def display_index():
    return [
        dbc.Jumbotron([
            html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            html.Div([
                dcc.Markdown("""
                [delivery Data Science Chair @UCLouvain](https://uclouvain.be/fr/chercher/fondation-louvain/actualites/creation-de-la-chaire-de-recherche-delivery-en-data-science.html)
                                 """)
            ], className="index_first"),
            dcc.Markdown(
                """
                Private comment

                """)
        ]),
    ]


def display_about():
    return [html.H1([html.Img(src='/assets/covidata.png'), "Covidata.be"], className="logo_index"),
            dcc.Markdown(
            """
            We are a team specialized in [AI, Analytics](https://aia.info.ucl.ac.be/people/) and [Computer Science](https://uclouvain.be/fr/instituts-recherche/icteam/ingi) from @UCLouvain_be and @EPL_UCLouvain.
            We produce this website with the hope it can help to better understand and objectively analyze the impact of the COVID crisis on Belgium e-comerce behavior.
            
            Please do not share the URL of this website yet.
            
            The current contributors to this project are:

 
            - [Pierre Schaus, Prof@UCLouvain](https://www.info.ucl.ac.be/~pschaus)
            - [Siegfried Nijssen, Prof@UCLouvain](https://www.info.ucl.ac.be/~snijssen/)
            - [Gael Aglin, PhD@UCLouvain](https://aia.info.ucl.ac.be)
            - [Vianney Coppé, PhD@UCLouvain](https://aia.info.ucl.ac.be)
            - [Guillaume Derval, PhD@UCLouvain](https://aia.info.ucl.ac.be)
            
            """)
    ]





index_menu = AppMenu('index', '', [
    AppLink(lazy_gettext("Home"), lazy_gettext("Home"), '/index', display_index),
    AppLink(lazy_gettext("About"), lazy_gettext("About"), '/about', display_about)
], fake_menu=True)
