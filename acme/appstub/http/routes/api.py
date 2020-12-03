from uvicore.http import ApiRouter, Routes
from uvicore.support.dumper import dump, dd


class Api(Routes[ApiRouter]):

    endpoints: str = 'acme.appstub.http.api'

    def register(self):
        # Available instance variables:
        # self.app, self.package, self.Router, self.prefix

        # If you defined a self.endpoints you can use string based module lookup
        self.include('welcome', tags=['Welcome'])

        # Or just import the module and pass in the route directly
        #from mreschke.wiki.http.endpoints import user
        #self.include(user.route, tags=['Users'])

        # If you really want to define inline routes, do it like this
        # route = self.Router()
        # @route.get('/hello')
        # async def hello():
        #     return {"hello":"world"}
        # self.include(route, tags=['extra'])

        # Example adding a second router to define different tags
        # Simply make a new Router() and another self.include()
        # route = self.Router()
        # @route.get('/hello2')
        # async def hello2():
        #     return {"hello":"world2"}
        # self.include(route, tags=['extra2'])
