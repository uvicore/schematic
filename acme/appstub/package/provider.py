import uvicore
from uvicore.package import Provider
from uvicore.support.dumper import dump, dd
from uvicore.console.package.registers import Cli
<provider-imports>

@uvicore.provider()
class Appstub(Provider, Cli<provider-class>):

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
            {'key': self.name, 'value': self.package_config},
            #{'key': self.name, 'module': 'acme.appstub.config.package.config'},

            # Example of how to override another packages config with your own.
            #{'key': 'uvicore.auth', 'module': 'acme.appstub.config.packages.auth.config'},
        ])

    def boot(self) -> None:
        """Bootstrap package into the uvicore framework.
        Boot takes place after ALL packages are registered.  This means all package
        configs are deep merged to provide a complete and accurate view of all
        configuration. This is where you register, connections, models,
        views, assets, routes, commands...  If you need to perform work after ALL
        packages have booted, use the event system and listen to the booted event:
        self.events.listen('uvicore.foundation.events.app.Booted', self.booted)"""

        # Define Provider Registrations
        self.registers(self.package.config.registers)
        <provider-db-connections>
        # Define view and asset paths and configure the templating system
        self.register_views()

        # Define Web and API routes and prefixes
        self.register_routes()

        # Define CLI commands to be added to the ./uvicore command line interface
        self.register_commands()

    def register_views(self) -> None:
        """Register HTTP view and asset paths and configure the Web templating system"""

        # Define view paths
        self.register_http_views(['acme.appstub.http.views'])

        # Define view composers - multiple calls to self.composers() are appended
        #self.register_http_view_composers('acme.appstub.http.composers.layout.Layout', 'appstub/*')
        #self.register_http_view_composers('acme.appstub.http.composers.layout.Layout', ['appstub/home', 'appstub/about'])

        # You can also define view composers as a dict
        # self.register_http_view_composers({
        #     'acme.appstub.http.composers.layout.Layout': 'appstub/*',
        #     'acme.appstub.http.composers.layout.Layout': ['appstub/home', 'appstub/about'],
        # })

        # Define public paths
        self.register_http_public(['acme.appstub.http.public'])

        # Define asset paths
        self.register_http_assets(['acme.appstub.http.public.assets'])

        # Define custom template options
        # def url_method(context: dict, name: str, **path_params: any) -> str:
        #     request = context["request"]
        #     return request.url_for(name, **path_params)

        # def up_filter(input):
        #     return input.upper()

        # def up_filter2(context, input):
        #     return input.upper()

        # def is_prime(n):
        #     import math
        #     if n == 2:
        #         return True
        #     for i in range(2, int(math.ceil(math.sqrt(n))) + 1):
        #         if n % i == 0:
        #             return False
        #     return True

        # self.register_http_view_context_processors({
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

    def register_routes(self) -> None:
        """Register Web and API routes and prefixes"""

        # Define web routes
        self.register_http_web_routes(
            module='acme.appstub.http.routes.web.Web',
            prefix=self.package.config.web.prefix,
            #name_prefix=None,
        )

        # Define api routes
        self.register_http_api_routes(
            module='acme.appstub.http.routes.api.Api',
            prefix=self.package.config.api.prefix,
            #name_prefix='api',
        )

    def register_commands(self) -> None:
        """Register CLI commands to be added to the ./uvicore command line interface"""

        # You can define CLI groups and commands as a complete dictionary
        # self.register_cli_commands({
        #     'appstub': {
        #         'help': 'Appstub Commands',
        #         'commands': {
        #             'welcome': 'acme.appstub.commands.welcome.cli',
        #         },
        #     },
        # })

        # Or you can define commands as kwargs (multiple calls to self.commands() are appended)
        self.register_cli_commands(
            group='appstub',
            help='Appstub Commands',
            commands={
                'welcome': 'acme.appstub.commands.welcome.cli',
            },
        )
