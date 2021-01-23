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
                'host': '127.0.0.1',
                'port': 3306,
                'database': 'appstub',
                'username': 'root',
                'password': 'techie',
                'prefix': 'auth_',
            },
        },
    },
}
