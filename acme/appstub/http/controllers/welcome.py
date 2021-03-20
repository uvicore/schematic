import uvicore
from uvicore.http import Request, response
from uvicore.http.routing import WebRouter, Controller


@uvicore.controller()
class Welcome(Controller):

    def register(self, route: WebRouter):

        @route.get('/', name='welcome')
        async def welcome(request: Request):
            # Example Jinja2 Template
            return response.View('appstub/welcome.j2', {
                'request': request
            })

            # Other example responses
            #return response.Text('Text Here')
            #return response.HTML('<b>HTML</b> here')
            #return response.JSON({'json':'here'})
            #return response.UJSON({'json':'here'}) # requiest ujson dependency
            # and more ...

        # Return router
        return route
