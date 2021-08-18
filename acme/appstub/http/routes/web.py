import uvicore
from uvicore.http.routing import Routes, WebRouter


@uvicore.routes()
class Web(Routes):

    # Apply scopes to all routes and children controllers
    #scopes = ['authenticated', 'employee']

    def register(self, route: WebRouter):
        """Register Web Route Endpoints"""

        # Define controller base path
        route.controllers = 'acme.appstub.http.controllers'

        # Public Routes
        route.controller('welcome')

        # Example of Private Routes
        # @route.group(scopes=['authenticated'])
        # def private_routes():
        #     route.controller('private_controller')

        # Return router
        # Must always return the router at the end of every controller and routes file
        # as this is one infinitely recursive nested router configuration.
        return route
