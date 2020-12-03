import uvicore
from uvicore.package import ServiceProvider


@uvicore.provider()
class Appstub(ServiceProvider):

    def register(self) -> None:
        """Register package into uvicore framework.
        All packages are registered before the framework boots.  This is where
        you define your packages configs and IoC bindings.  Configs are deep merged only after
        all packages are registered.  No real work should be performed here as it
        is very early in the bootstraping process and most internal processes are not
        instantiated yet."""

        # Register configs
        # If config key already exists items will be deep merged allowing
        # you to override small peices of other package configs
        self.configs([
            # Here self.name is your packages name (ie: mreschke.wiki).
            {'key': self.name, 'module': 'acme.appstub.config.appstub.config'},

            # Override uvicore.auth config to customize the auth database connection
            {'key': 'uvicore.auth', 'module': 'acme.appstub.config.auth.config'},
        ])

    def boot(self) -> None:
        """Bootstrap package into uvicore framework.
        Boot takes place after all packages are registered.  This means all package
        configs are deep merged to provide a complete and accurate view of all configs.
        This is where you load views, assets, routes, commands..."""

        # Define all tables/models used by this package
        # The goal is to load up all SQLAlchemy tables for complete metedata definitions.
        # If you separate tables vs models use self.tables(['myapp.database.tables.*])
        # If you use models only, or models with inline tables then use self.models(['myapp.models.*])
        # Order does not matter as they are sorted topologically for ForeignKey dependencies
        # self.tables([
        #     'acme.appstub.database.tables.*',
        # ])

        # Define data seeders used by this package
        # self.seeders([
        #     'acme.appstub.database.seeders.seeders.seed',
        # ])

        # Define view and asset paths and configure the templating system
        self.load_views()

        # Define Web and API routers
        self.load_routes()

        # Define CLI commands to be added to the ./uvicore command line interface
        self.load_commands()

    def load_views(self) -> None:
        """Define view and asset paths and configure the templating system"""

        # Add view paths
        self.views(['acme.appstub.http.views'])

        # Add asset paths
        self.assets([
            'acme.appstub.http.static',
        ])

        # Add custom template options
        self.template({
            # 'context_functions': [
            #     {'name': 'url2', 'method': url_method}
            # ],
            # 'context_filters': [
            #     {'name': 'up', 'method': up_filter2}
            # ],
            # 'filters': [
            #     {'name': 'up', 'method': up_filter}
            # ],
            # 'tests': [
            #     {'name': 'prime', 'method': is_prime}
            # ],
        })
        # Optionally, hack jinja to add anything possible like so
        #app.jinja.env.globals['whatever'] = somefunc

    def load_routes(self) -> None:
        """Define Web and API router"""

        self.web_routes('acme.appstub.http.routes.web.Web')
        self.api_routes('acme.appstub.http.routes.api.Api')

    def load_commands(self) -> None:
        """Define CLI commands to be added to the ./uvicore command line interface"""

        self.commands([
            {
                'group': {
                    'name': 'appstub',
                    'parent': 'root',
                    'help': 'Appstub Commands',
                },
                'commands': [
                    {'name': 'welcome', 'module': 'acme.appstub.commands.welcome.cli'},
                ],
            },
        ])
