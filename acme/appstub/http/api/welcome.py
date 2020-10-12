from typing import List
from uvicore.http.routing import ApiRouter

route = ApiRouter()

@route.get('/welcome')
async def welcome():
    return {'welcome': 'to uvicore API!'}
