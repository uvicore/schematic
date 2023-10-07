from .auth import auth
from .mail import mail
from .cache import cache
from .logger import logger
from .overrides import overrides
from .http import web, api, server
from uvicore.configuration import env
from uvicore.typing import OrderedDict


# --------------------------------------------------------------------------
# Running Application Configuration
#
# This config only applies if this package is RUNNING as the main application
# (a CLI command or the HTTP server).  If this package is included in another
# running app (as a library), these app configs are NOT used at all.  If your
# package is ONLY a library and will never have any CLI or HTTP entrypoints
# then you can safely delete this app.py and all the individual .py configs
# that it imports (auth, mail, cache, logger, overrides, http etc...)
# Accessible at config('app.name')
# --------------------------------------------------------------------------
config = {

    # --------------------------------------------------------------------------
    # Running App Information
    #
    # name: The human readable name of this package/app.  Like 'Matts Wiki'
    # main: The package provider to run when this app is served/executed
    # --------------------------------------------------------------------------
    'name': env('APP_NAME', 'Appstub App'),
    'debug': env.bool('DEBUG', False),
    'main': {
        'package': 'acme.appstub',
        'provider': 'acme.appstub.package.provider.Appstub'
    },


    # --------------------------------------------------------------------------
    # Pretty Printer Configuration
    #
    # Default width if not defined is 120
    # --------------------------------------------------------------------------
    # 'dump': {
    #     'width': 120
    # },


    # --------------------------------------------------------------------------
    # Include All Other App Level Configs
    #
    # Split out into multiple files for a better user experience
    # --------------------------------------------------------------------------
    'server': server,
    'web': web,
    'api': api,
    'auth': auth,
    'overrides': overrides,
    'mail': mail,
    'cache': cache,
    'logger': logger,
}
