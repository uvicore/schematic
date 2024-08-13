from uvicore.configuration import env
from uvicore.typing import OrderedDict


# --------------------------------------------------------------------------
# Database Connections
#
# Uvicore allows for multiple database connections (backends) each with
# their own connection name.  Use 'default' to set the default connection.
# Database doesn't just mean a local relational DB connection.  Uvicore
# ORM can also query remote APIs, CSVs, JSON files and smash them all
# together as if from a local database join!
# --------------------------------------------------------------------------
database = {
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
            # All options are passed directly to the specific dialects connector.
            'options': {
                'ssl': env.bool('DB_APPSTUB_SSL', False),
            }
        },

        # Example of ORM over Remote Uvicore API
        # 'appstub': {
        #     'driver': 'api',
        #     'dialect': 'uvicore',
        #     'url': 'https://appstub.example.com/api',
        #     'prefix': None
        # },
    },
}


# --------------------------------------------------------------------------
# Redis Connections
#
# Uvicore allows for multiple redis connections (backends) each with
# their own connection name.  Use 'default' to set the default connection.
# --------------------------------------------------------------------------
redis = {
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
}
