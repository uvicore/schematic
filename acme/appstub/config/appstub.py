# This is the main appstub config.  All items here can be overridden
# when used inside other applications.  Accessible at config('acme.appstub')

config = {

    # --------------------------------------------------------------------------
    # Registration Control
    # --------------------------------------------------------------------------
    # This lets you control the service provider registrations.  If this app
    # is used as a package inside another app you might not want some things
    # registered in that context.
    'register_web_routes': True,
    'register_api_routes': True,
    'register_views': True,
    'register_assets': True,
    'register_commands': True,


    # --------------------------------------------------------------------------
    # Route Configuration
    # --------------------------------------------------------------------------
    # Or like so, no underscores, so in dot notation config('blog.route.prefix')
    # have to do deep merges
    'route': {
        'web_prefix': '',
        'api_prefix': '/api',
    },


    # --------------------------------------------------------------------------
    # Database Connections
    # --------------------------------------------------------------------------
    'database': {
        'default': 'appstub',
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
                'host': '127.0.0.1',
                'port': 3306,
                'database': 'uvicore_appstub',
                'username': 'root',
                'password': 'techie',
                'prefix': None,
            },
        },
    },
}
