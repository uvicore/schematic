import uvicore
from uvicore.http.routing import Routes, ApiRouter, ModelRouter


@uvicore.routes()
class Api(Routes):

    # Apply scopes to all routes and children controllers
    #scopes = ['authenticated', 'employee']

    def register(self, route: ApiRouter):
        """Register API Route Endpoints"""

        # Define controller base path
        route.controllers = 'acme.appstub.http.api'

        # Include dynamic model CRUD API endpoints (the "auto API")!
        @route.group()
        def autoapi():
        #def autoapi(scopes=['authenticated']):
            route.include(ModelRouter)

        # Public Routes
        route.controller('welcome')

        # Example of Private Routes
        # @route.group(scopes=['authenticated'])
        # def private_routes():
        #     route.controller('private_controller')

        # Return router
        return route
