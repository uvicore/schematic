from uvicore.http.routing import WebRouter, Routes
from uvicore.http import Request, response
from uvicore.support.dumper import dump, dd
from uvicore import app, config


class Web(Routes[WebRouter]):

    endpoints: str = 'acme.appstub.http.controllers'

    def register(self):
        # String style
        self.include('welcome')

        # Import style
        #from mreschke.wiki.http.controllers import about
        #self.include(about.route)

        # Define inline routes
        # route = self.Router()
        # @route.get('/welcome-text')
        # async def about(request: Request):
        #     return response.Text('Welcome in plain text')
        # self.include(route)
