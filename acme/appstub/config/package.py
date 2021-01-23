from uvicore.typing import OrderedDict

# This is the main appstub config.  All items here can be overridden
# when used inside other applications.  Accessible at config('acme.appstub')

config = {

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
                'database': 'appstub',
                'username': 'root',
                'password': 'techie',
                'prefix': None,
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
    # requires them.  Services like uvicore.database, uvicore.orm, uvicore.http
    # uvicore.auth...
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
