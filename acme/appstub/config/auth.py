from uvicore.configuration import env

# Example of overriding the uvicore.auth package config to adjust
# the auth database connection and prefix

config = {
    # --------------------------------------------------------------------------
    # Database Connections
    # --------------------------------------------------------------------------
    'database': {
        'connections': {
            # SQLite Example
            # 'auth': {
            #     'driver': 'sqlite',
            #     'database': ':memory',
            #     'prefix': 'auth_',
            # },

            # MySQL Example
            'auth': {
                'driver': 'mysql',
                'dialect': 'pymysql',
                'host': env('MYSQL_AUTH_HOST', '127.0.0.1'),
                'port': env.int('MYSQL_AUTH_PORT', 3306),
                'database': env('MYSQL_AUTH_DB', 'appstub'),
                'username': env('MYSQL_AUTH_USER', 'root'),
                'password': env('MYSQL_AUTH_PASSWORD', 'techie'),
                'prefix': env('MYSQL_AUTH_PREFIX', 'auth_'),
            },
        },
    },
}
