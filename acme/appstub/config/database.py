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
        'appstub': {
            'backend': env('DB_APPSTUB_BACKEND', 'sqlalchemy'),
            'dialect': env('DB_APPSTUB_DIALECT', 'sqlite'),
            'driver': env('DB_APPSTUB_DRIVER', 'aiosqlite'),
            'database': env('DB_APPSTUB_DB', ':memory:'),
            'prefix': env('DB_APPSTUB_PREFIX', None),
        },

        # MySQL Example
        # 'appstub': {
        #     'backend': 'sqlalchemy',
        #     'dialect': env('DB_APPSTUB_DIALECT', 'mysql'),
        #     'driver': env('DB_APPSTUB_DRIVER', 'aiomysql'),
        #     'host': env('DB_APPSTUB_HOST', '127.0.0.1'),
        #     'port': env.int('DB_APPSTUB_PORT', 3306),
        #     'database': env('DB_APPSTUB_DB', 'appstub'),
        #     'username': env('DB_APPSTUB_USER', 'root'),
        #     'password': env('DB_APPSTUB_PASSWORD', 'techie'),
        #     'prefix': env('DB_APPSTUB_PREFIX', None),
        #     # All options passed directly as **kwargs to the backends connect, create_pool,
        #     # create_engine or other backend specific create methods
        #     # 'options': {
        #     #     'connect_args': {
        #     #         'ssl': {}
        #     #     }
        #     # },
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
