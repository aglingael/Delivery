from flask_babel import lazy_gettext

from pages import AppMenu, AppLink
from pages.delivery.volumes import display_volumes
from pages.delivery.success import display_success
from pages.delivery.new_clients import display_new_clients
from pages.delivery.apr_feb import display_apr_feb


delivery_menu = AppMenu(lazy_gettext("delivery"), "/delivery", [
    AppLink(lazy_gettext("Volumes"), lazy_gettext("Volumes"), "/volumes", display_volumes),
    AppLink(lazy_gettext("Success Rates"), lazy_gettext("Success Rates"), "/success", display_success),
    AppLink(lazy_gettext("April vs February"), lazy_gettext("April vs February"), "/apr_feb", display_apr_feb),
    AppLink(lazy_gettext("New customers"), lazy_gettext("New customers"), "/new_clients", display_new_clients),
])
