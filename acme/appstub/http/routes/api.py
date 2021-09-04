import uvicore
from uvicore.http.routing import Routes, ApiRouter, ModelRouter

# Extra
# from uvicore.auth import UserInfo
# from uvicore.http.routing import Guard
# from uvicore.typing import Dict, List, Optional
# from uvicore.http.exceptions import HTTPException
# from uvicore.http.params import Path, Query, Header, Cookie, Body, Form, File, Depends, Security


@uvicore.routes()
class Api(Routes):

    # --------------------------------------------------------------------------
    # Example:  Multiple ways to apply route level middleware including
    # auth guards with scoped permissions to this entire controller.
    # Tip: Your routes/api.py and routes/web.py are actually the same
    # as controllers.  In fact controllers are just nested routers.  So all
    # notes here also apply to your routes/* files and controllers.
    # --------------------------------------------------------------------------
    # Apply scopes to all routes and children controllers - simple and preferred
    #scopes = ['authenticated', 'employee']

    # Scopes is a shortcut to
    #auth = Guard(['authenticated', 'gardner'])

    # Scopes and auth are shortcuts to the full middleware stack
    # middleware = [
    #     Guard(['authenticated', 'post_manager']),
    #     Any other route based middleware here
    # ]

    # Optionally, apply scopes and also grab the current user
    # user: UserInfo = Guard(['authenticated'])
    #   Then in your routes, inject the user with
    #   async def welcome(request: Request, user: UserInfo = self.user):

    def register(self, route: ApiRouter):
        """Register API Route Endpoints"""

        # Define controller base path
        route.controllers = 'acme.appstub.http.api'

        # Public Routes
        route.controller('welcome')

        # Include dynamic model CRUD API endpoints (the "auto API")!
        # These routes are automatically protected by model.crud style permissions.
        route.include(ModelRouter, options=uvicore.config.acme.appstub.api.auto_api)



        # ----------------------------------------------------------------------
        # Example: Routes vs controllers vs api controllers
        # Technically, there is no difference between your routes files
        # and controllers or api controllers.  They are all just one huge nested
        # router.  This means you could have ALL your routes right here in this
        # file, or you can break them out into controllers using the
        # .controller() or its alias .include() methods
        # ----------------------------------------------------------------------
        # route.controller('acme.appstub.http.controllers.some.other.Other')

        # Also, route.controller and route.include are aliases of each other, same thing.
        # route.include('acme.appstub.http.controllers.some.other2.Other2')

        # Instead of typing the full module path, if route.controllers is defined
        # Then all .controller() and .include() can use relative paths
        # route.controllers = 'acme.appstub.http.controllers'

        # Looks for Class in acme.appstub.http.controllers.some.Some
        # route.controller('some')

        # Leading period means APPEND path to defined route.controllers
        # So this looks for acme.appstub.http.controllers.other3.Other3
        # route.controller('.other3.Other3')

        # If no leading . but other . exists, then it is assuming a full path,
        # regardless if route.controllers is defined or not.


        # ----------------------------------------------------------------------
        # Example: Private routes protected by scopes (permissions)
        # ----------------------------------------------------------------------
        # route.group(scopes=['authenticated'])
        # def private():
        #     route.controller('posts')


        # ----------------------------------------------------------------------
        # Example: Grouping routes for common paths and scopes
        # ----------------------------------------------------------------------
        # route.group('/group1', scopes=['authenticated'], tags=['Group1'])
        # def group1():
        #     # All routes in these sub controllers will have Tag=Group1 and path
        #     # prefix of /group1/* with route name appstub.group1.*
        #     route.controller('users')
        #     route.controller('tags')

        #     # Nested groups work as expected
        #     route.group('/subgroup1', scopes=['admin'], tags=['Subgroup1'])
        #     def subgroup1():
        #         # Routes here have merged scopes ['authenticated', 'admin']
        #         # Will show up in tags Group1 and Subgroup1
        #         # Will have path of /group1/subgroup1.*
        #         # Will be route names appstub.group1.subgroup1.*
        #         route.controller('hashtags')


        # ----------------------------------------------------------------------
        # Example: controller() and include() methods also accept prefix and tags
        # Must like a @route.group() would.  It does not accept scopes, auth or
        # other route based middleware, use groups for that.
        # ----------------------------------------------------------------------
        # route.include('admin', prefix='/admin', tags=['Admin'])


        # ----------------------------------------------------------------------
        # Example: Changing the route name
        # Each route is given a name automatically.  A name is what you can use
        # to reference the route in your code and view templates.  Try to use the
        # route name instead of the path as paths WILL change as other users use
        # your library because they can tweak the BASE PATH.  Views should be using
        # {{ url('acme.ex0')}}, never /example0
        # If you don't specify a name, uvicore makes a name automatically
        # from the path, even nested paths from groups.  Name always starts
        # with your apps name, ie: acme.
        # ----------------------------------------------------------------------
        # Names work on include() or its alias controller(), or in groups
        #route.include('example0', name='ex0' prefix='/profile', tags=['Admin'])
        # @route.group('/group2', name='g2'):
        # def group2():
        #     # Name will be acme.g2.ex0 instead of the auto named acme.group2.example0
        #     route.get('/example0', example0_method, name='ex0'),


        # ----------------------------------------------------------------------
        # Example: Using route methods instead of decorators
        # Don't like route decorators anywhere?  Thats fine, you can use a large
        # route dictionary style.
        # ----------------------------------------------------------------------
        # route.get('/example1', some_method)
        # route.group('/group3', scopes=['authenticated'], routes=[
        #     route.get('/example2', some_method2),
        #     route.get('/example3', some_method3),
        # ])


        # ----------------------------------------------------------------------
        # Example: Auto model API. Remove auto.crud scopes.  Setting scopes
        # to [] makes the auto API wide open (no permissions required)
        # ----------------------------------------------------------------------
        # route.include(ModelRouter, options={
        #     'scopes': []
        # })


        # ----------------------------------------------------------------------
        # Example: Auto model API. Set scopes manually, no auto.crud scopes used.
        # ----------------------------------------------------------------------
        # route.include(ModelRouter, options={
        #     'scopes': ['autoapi_user']
        # })

        # ----------------------------------------------------------------------
        # Example: Auto model API. APPEND these scopes to the auto.crud scopes
        # So ends up being something like ['post.read', 'and_this_scope']
        # ----------------------------------------------------------------------
        # @route.group(scopes=['and_this_scope'])
        # def autoapi():
        #     route.include(ModelRouter)



        # Return router
        # Must always return the router at the end of every controller and routes file
        # as this is one infinitely recursive nested router configuration.
        return route
