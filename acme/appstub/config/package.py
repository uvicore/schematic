from uvicore.configuration import env
from uvicore.typing import OrderedDict

# This is the main appstub config.  All items here can be overridden
# when used inside other applications.  Accessible at config('acme.appstub')

config = {

    # --------------------------------------------------------------------------
    # Package Custom Configuration
    #
    # Your custom package specific configs go here
    # --------------------------------------------------------------------------
    # 'example': 'accessible at acme.appstub.example',


    # --------------------------------------------------------------------------
    # Package Information
    #
    # Most other info like name, short_name, vendor are derived automatically
    # --------------------------------------------------------------------------
    'version': '0.1.0',


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
    # prefix: All api routes will be prefixed with this URI. Ex: '' or '/wiki'
    # --------------------------------------------------------------------------
    'api': {
        'prefix': '',
    },


    # --------------------------------------------------------------------------
    # Database Connections
    #
    # Database doesn't just mean a local relational DB connection.  Uvicore
    # ORM can also query remote APIs, CSVs, JSON files and smash them all
    # together as if from a local database join!
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
                'driver': env('DB_APPSTUB_DRIVER', 'mysql'),
                'dialect': env('DB_APPSTUB_DIALECT', 'pymysql'),
                'host': env('DB_APPSTUB_HOST', '127.0.0.1'),
                'port': env.int('DB_APPSTUB_PORT', 3306),
                'database': env('DB_APPSTUB_DB', 'appstub'),
                'username': env('DB_APPSTUB_USER', 'root'),
                'password': env('DB_APPSTUB_PASSWORD', 'techie'),
                'prefix': env('DB_APPSTUB_PREFIX', None),
            },

            # Example of ORM over Remote Uvicore API
            # 'appstub': {
            #     'driver': 'api',
            #     'dialect': 'uvicore',
            #     'url': 'https://appstub.example.com/api',
            #     'prefix': None
            # },
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
    # minimal and only depends on configuration, logging and console itself.
    # You must add other core services built into uvicore only if your package
    # requires them.  Services like uvicore.database, uvicore.orm, uvicore.auth
    # uvicore.http, etc...
    # --------------------------------------------------------------------------
    'dependencies': OrderedDict({
        # Foundation is the core of uvicore and is required as the first dependency.
        # Foundation itself relys on configuration, logging, console, cache and more.
        'uvicore.foundation': {
            'provider': 'uvicore.foundation.services.Foundation',
        },

        # Redis provides redis access and redis caching if enabled in your app config
        # 'uvicore.redis': {
        #     'provider': 'uvicore.redis.services.Redis',
        # },

        # Database is required for database queries and the ORM.  Disable if your project
        # does not require database or models
        'uvicore.database': {
            'provider': 'uvicore.database.services.Database',
        },

        # ORM provides an object relationional mapper between your databse tables
        # and your ORM models.  Disable if your project does not require Models.
        # Even without the ORM, you can still use the database with the db query builder.
        'uvicore.orm': {
            'provider': 'uvicore.orm.services.Orm',
        },

        # Auth provides all of the auth middleware, user providers, authenticators and guards
        'uvicore.auth': {
            'provider': 'uvicore.auth.services.Auth',
        },

        # HTTP provides API and WEB endpoints, assets, templates.  A full webserver.
        'uvicore.http': {
            'provider': 'uvicore.http.services.Http',
        },

        # HTTP async client based on aiohttp.  Enable this package if you need
        # to query other HTTP endpoints in your package.
        # 'uvicore.http_client': {
        #     'provider': 'uvicore.http_client.services.HttpClient',
        # },
    }),

}
