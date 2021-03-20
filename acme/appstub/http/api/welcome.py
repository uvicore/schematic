import uvicore
from uvicore.http.routing import ApiRouter, Controller


@uvicore.controller()
class Welcome(Controller):

    def register(self, route: ApiRouter):

        @route.get('/welcome', tags=['Welcome'])
        async def welcome():
            return {'welcome': 'to uvicore API!'}

        # Return router
        return route
