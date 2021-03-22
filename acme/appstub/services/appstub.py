import uvicore
from uvicore.package import ServiceProvider
from uvicore.http.provider import Http
from uvicore.database.provider import Db
from uvicore.redis.provider import Redis
from uvicore.console.provider import Cli
from uvicore.support.dumper import dump, dd


@uvicore.provider()
class Appstub(ServiceProvider, Cli, Db, Redis, Http):

    def register(self) -> None:
        """Register package into the uvicore framework.
        All packages are registered before the framework boots.  This is where
        you define your packages configs, IoC bindings and early event listeners.
        Configs are deep merged only after all packages are registered.  No real
        work should be performed here as it is very early in the bootstraping
        process and we have no clear view of the full configuration system."""

        # Register configs
        # If config key already exists items will be deep merged allowing
        # you to override granular aspects of other package configs
        self.configs([
            # Here self.name is your packages name (ie: acme.appstub).
            {'key': self.name, 'module': 'acme.appstub.config.package.config'},

            # Override uvicore.auth config to customize the auth database connection
            {'key': 'uvicore.auth', 'module': 'acme.appstub.config.auth.config'},
        ])

    def boot(self) -> None:
        """Bootstrap package into the uvicore framework.
        Boot takes place after ALL packages are registered.  This means all package
        configs are deep merged to provide a complete and accurate view of all
        configuration. This is where you register, connections, models,
        views, assets, routes, commands...  If you need to perform work after ALL
        packages have booted, use the event system and listen to the booted event:
        self.events.listen('uvicore.foundation.events.app.Booted, self.booted')"""

        # Define Service Provider Registrations
        self.registers(self.package.config.registers)

        # Define Database Connections
        self.connections(
            connections=self.package.config.database.connections,
            default=self.package.config.database.default
        )

        # Define Redis Connections
        self.redis_connections(
            connections=self.package.config.redis.connections,
            default=self.package.config.redis.default
        )

        # Define all tables or models
        # The goal is to load up all SQLAlchemy tables for complete metedata definitions.
        # If you separate tables vs models use self.tables(['myapp.database.tables])
        # If you use models only, or models with inline tables then use self.models(['myapp.models])
        # Order does not matter as they are sorted topologically for ForeignKey dependencies
        # If you don't have an __init__.py index in your tables or models you can use
        # wildcard imports self.models(['myapp.models.*])
        self.models([
            'acme.appstub.models',
        ])
        # self.tables([
        #     'acme.appstub.database.tables',
        # ])

        # Define data seeders
        # self.seeders([
        #     'acme.appstub.database.seeders.seed',
        # ])

        # Define view and asset paths and configure the templating system
        self.define_views()

        # Define Web and API routes and prefixes
        self.define_routes()

        # Define CLI commands to be added to the ./uvicore command line interface
        self.define_commands()

    def define_views(self) -> None:
        """Define view and asset paths and configure the templating system"""

        # Define view paths
        self.views(['acme.appstub.http.views'])

        # Define public paths
        self.public(['acme.appstub.http.public'])

        # Define asset paths
        self.assets(['acme.appstub.http.public.assets'])

        # Define custom template options
        # self.template({
        #     'context_functions': {
        #         'url2': url_method,
        #     },
        #     'context_filters': {
        #         'up': up_filter2,
        #     },
        #     'filters': {
        #         'up': up_filter,
        #     },
        #     'tests': {
        #         'prime': is_prime,
        #     },
        # })
        # Optionally, hack jinja to add anything possible like so
        #app.jinja.env.globals['whatever'] = somefunc

    def define_routes(self) -> None:
        """Define Web and API routes and prefixes"""

        # Define web routes
        self.web_routes(
            module='acme.appstub.http.routes.web.Web',
            prefix=self.package.config.web.prefix,
            #name_prefix=None,
        )

        # Define api routes
        self.api_routes(
            module='acme.appstub.http.routes.api.Api',
            prefix=self.package.config.api.prefix,
            #name_prefix='api',
        )

    def define_commands(self) -> None:
        """Define CLI commands to be added to the ./uvicore command line interface"""

        # You can define CLI groups and commands as a complete dictionary
        # self.commands({
        #     'appstub': {
        #         'help': 'Appstub Commands',
        #         'commands': {
        #             'welcome': 'acme.appstub.commands.welcome.cli',
        #         },
        #     },
        # })

        # Or you can define commands as kwargs (multiple calls to self.commands() are appended)
        self.commands(
            group='appstub',
            help='Appstub Commands',
            commands={
                'welcome': 'acme.appstub.commands.welcome.cli',
            },
        )
