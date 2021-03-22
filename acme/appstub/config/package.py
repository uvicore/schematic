from uvicore.configuration import env
from uvicore.typing import OrderedDict

# This is the main appstub config.  All items here can be overridden
# when used inside other applications.  Accessible at config('acme.appstub')

config = {

    # --------------------------------------------------------------------------
    # Web Configuration
    #
    # prefix: All web routes will be prefixed with this URI. Ex: '' or '/wiki'
    # --------------------------------------------------------------------------
    'web': {
        'prefix': '',
    },

    # --------------------------------------------------------------------------
    # Api Configuration
    #
    # prefix: All web routes will be prefixed with this URI. Ex: '' or '/wiki'
    # --------------------------------------------------------------------------
    'api': {
        'prefix': '',
    },


    # --------------------------------------------------------------------------
    # Database Connections
    # --------------------------------------------------------------------------
    'database': {
        'default': env('DATABASE_DEFAULT', 'appstub'),
        'connections': {
            # SQLite Example
            # 'appstub': {
            #     'driver': 'sqlite',
            #     'database': ':memory',
            #     'prefix': None,
            # },

            # MySQL Example
            'appstub': {
                'driver': 'mysql',
                'dialect': 'pymysql',
                'host': env('MYSQL_APPSTUB_HOST', '127.0.0.1'),
                'port': env.int('MYSQL_APPSTUB_PORT', 3306),
                'database': env('MYSQL_APPSTUB_DB', 'appstub'),
                'username': env('MYSQL_APPSTUB_USER', 'root'),
                'password': env('MYSQL_APPSTUB_PASSWORD', 'techie'),
                'prefix': env('MYSQL_APPSTUB_PREFIX', None),
            },
        },
    },


    # --------------------------------------------------------------------------
    # Redis Connections
    # --------------------------------------------------------------------------
    'redis': {
        'default': env('REDIS_DEFAULT', 'appstub'),
        'connections': {
            'appstub': {
                'host': env('REDIS_APPSTUB_HOST', '127.0.0.1'),
                'port': env.int('REDIS_APPSTUB_PORT', 6379),
                'database': env.int('REDIS_APPSTUB_DB', 0),
                'password': env('REDIS_APPSTUB_PASSWORD', None),
            },
            'cache': {
                'host': env('REDIS_CACHE_HOST', '127.0.0.1'),
                'port': env.int('REDIS_CACHE_PORT', 6379),
                'database': env.int('REDIS_CACHE_DB', 2),
                'password': env('REDIS_CACHE_PASSWORD', None),
            },
        },
    },


    # --------------------------------------------------------------------------
    # Registration Control
    # --------------------------------------------------------------------------
    # This lets you control the service provider registrations.  If this app
    # is used as a package inside another app you might not want some things
    # registered in that context.  Use config overrides in your app to change
    # registrations
    # 'registers': {
    #     'web_routes': False,
    #     'api_routes': False,
    #     'middleware': False,
    #     'views': False,
    #     'assets': False,
    #     'commands': False,
    #     'models': False,
    #     'tables': False,
    #     'seeders': False,
    # },

    # --------------------------------------------------------------------------
    # Package Dependencies (Service Providers)
    #
    # Define all the packages that this package depends on.  At a minimum, only
    # the uvicore.foundation package is required.  The foundation is very
    # minimal and only depends on configuratino, logging and console itself.
    # You must add other core services built into uvicore only if your package
    # requires them.  Services like uvicore.database, uvicore.orm, uvicore.auth
    # uvicore.http, etc...
    # --------------------------------------------------------------------------
    'dependencies': OrderedDict({
        'uvicore.foundation': {
            'provider': 'uvicore.foundation.services.Foundation',
        },
        # 'uvicore.database': {calc
        #     'provider': 'uvicore.database.services.Database',
        # },
        # 'uvicore.orm': {
        #     'provider': 'uvicore.orm.services.Orm',
        # },
        # 'uvicore.auth': {
        #     'provider': 'uvicore.auth.services.Auth',
        # },
        'uvicore.http': {
            'provider': 'uvicore.http.services.Http',
        },
    }),

}
