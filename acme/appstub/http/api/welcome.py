import uvicore
from uvicore.http.routing import ApiRouter, Controller


@uvicore.controller()
class Welcome(Controller):

    def register(self, route: ApiRouter):

        @route.get('/welcome', tags=['Welcome'])
        async def welcome():
            return {'welcome': 'to uvicore API!'}

        # @route.get('/posts', tags=['Post'])
        # async def posts() -> List[Post]:
        #     return await Post.query().get()

        # @route.get('/post/{id}', tags=['Post'])
        # async def post(id: int) -> Post:

        # Return router
        return route
