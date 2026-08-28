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
            # If 'url' is defined using sqlalchemy backend,
            # it will be used instead of deriving one from the properties above.
            # 'url': '',
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
        #     # If 'url' is defined using sqlalchemy backend,
        #     # it will be used instead of deriving one from the properties above.
        #     'url': '',
        #     # All options passed directly as **kwargs to the backends connect, create_pool,
        #     # create_engine or other backend specific create methods
        #     # Example enable SSL using pymysql driver
        #     # 'options': {
        #     #     'ssl_ca': '/etc/ssl/certs/ca-certificates.crt',
        #     # },
        #     # Example enable SSL using aiomysql driver
        #     # 'options': {
        #     #     'ssl': True
        #     # }
        #     # Where 'options' configures the DRIVER (connect_args), 'pool' configures the
        #     # ENGINE's connection pool (SQLAlchemy's pool_* create_engine args).  Keys:
        #     # pre_ping, recycle, size, max_overflow, timeout, use_lifo, reset_on_return.
        #     # Only pre_ping is defaulted (True); an unknown key raises at bootstrap.
        #     # 'pool': {
        #     #     'pre_ping': True,       # ping a pooled conn before use (recovers from
        #     #                             # a connection the server closed while idle)
        #     #     'recycle': 3600,        # rebuild connections older than N seconds
        #     #     'size': 5,
        #     #     'max_overflow': 10,
        #     # },
        # },

        # Snowflake Example
        # 'appstub': {
        #     'backend': 'sqlalchemy',
        #     'dialect': env('DB_APPSTUB_DIALECT', 'snowflake'),
        #     'account': env('DB_APPSTUB_ACCOUNBT', ''),
        #     'database': env('DB_APPSTUB_DB', ''),
        #     'schema': env('DB_APPSTUB_SCHEMA', ''),
        #     'warehouse': env('DB_APPSTUB_WAREHOUSE', ''),
        #     'username': env('DB_APPSTUB_USER', ''),
        #     'password': env('DB_APPSTUB_PASSWORD', ''),
        #     'role': env('DB_APPSTUB_ROLE', ''),
        #     'options': {
        #         # If using a Private Key, replace all new lines with blanks (all on one string)
        #         # and remove -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----
        #         # Or take the .pem file and run it through a DER base64 to get a single string like so
        #         # openssl pkcs8 -in snowflake.pem -inform PEM -outform DER -nocrypt | base64 -w 0
        #         'private_key': env('DB_APPSTUB_PRIVATE_KEY', ''),
        #
        #         # Uvicore DEFAULTS these two on every snowflake connection - you do not
        #         # need to set them.  A Snowflake session's MASTER token expires after ~4h
        #         # and the connector does NOT renew it, so without a heartbeat any
        #         # long-running process starts failing every query with
        #         # '390114: Authentication token has expired'.  A heartbeat is a token-only
        #         # REST call: no query, no warehouse credits.  Uvicore also teaches the
        #         # engine that the terminal token codes are DISCONNECTS, so a token that
        #         # dies anyway invalidates the pool instead of being handed back out
        #         # forever.  Set either key here only to OVERRIDE the default (ex:
        #         # keep_alive False for a short-lived CLI).
        #         # 'client_session_keep_alive': True,
        #         # 'client_session_keep_alive_heartbeat_frequency': 900,
        #     }
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
            # Optional arbitrary client kwargs passed straight through to the
            # underlying redis.asyncio client (health_check_interval,
            # socket_timeout, max_connections, decode_responses, ...).
            # 'options': {
            #     'health_check_interval': 30,
            # },
        },
        'cache': {
            'host': env('REDIS_CACHE_HOST', '127.0.0.1'),
            'port': env.int('REDIS_CACHE_PORT', 6379),
            'database': env.int('REDIS_CACHE_DB', 2),
            'password': env('REDIS_CACHE_PASSWORD', None),
        },
    },
}
