import pytest
import uvicore
from uvicore.support.dumper import dump, dd


# ------------------------------------------------------------------------------
# Example: testing an API route
#
# This hits the stock welcome API endpoint registered in http/routes/api.py,
# which includes the api controller at http/api/welcome.py serving GET '/welcome'.
#
# Full path = your api 'prefix' (config/http.py, defaults to '/api')
#           + the route path ('/welcome')
#           = '/api/welcome'
#
# The `client` fixture (tests/conftest.py) gives you an httpx AsyncClient wired
# straight to your ASGI app - no running server needed.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_welcome_api_endpoint(client):
    res = await client.get('/api/welcome')

    # The stock welcome endpoint is public, so it returns 200
    assert res.status_code == 200, res.text

    # API routes wrap their payload in the APIResponse envelope
    # (see uvicore/http/response.py - api_version, response_ms, data, etc.).
    # Your actual return value lives under the 'data' key.
    body = res.json()
    assert 'data' in body
    data = body['data']

    # These mirror exactly what http/api/welcome.py returns
    assert data['hello'] == 'World!'
    assert 'welcome' in data                          # the current user's email
    assert data['to'] == f'Uvicore {uvicore.app.version}'
