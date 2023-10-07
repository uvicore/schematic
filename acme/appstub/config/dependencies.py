from uvicore.configuration import env
from uvicore.typing import OrderedDict


# --------------------------------------------------------------------------
# Package Dependencies (Package Providers)
#
# Define all the packages that this package depends on.  At a minimum, only
# the uvicore.foundation package is required.  The foundation is very minimal
# and only depends on configuration, logging and the console packages. You
# must add other core services built into uvicore only if your package
# requires them.  Services like uvicore.database, uvicore.orm, uvicore.auth
# uvicore.http, etc...
# --------------------------------------------------------------------------
dependencies = OrderedDict({
    # Foundation is the core of uvicore and is required as the first dependency.
    # Foundation itself relys on configuration, logging, console, cache and more.
    'uvicore.foundation': {
        'provider': 'uvicore.foundation.services.Foundation',
    },

    # HTTP async client based on aiohttp.
    'uvicore.http_client': {
        'provider': 'uvicore.http_client.services.HttpClient',
    },
    <package-dependencies>
})
