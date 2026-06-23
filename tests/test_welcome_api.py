import pytest
import uvicore
from uvicore.support.dumper import dump, dd


# ------------------------------------------------------------------------------
# Example: testing an API route
#
# Best practice (and what the docs recommend): reference a route by its NAME, not
# a hardcoded URL.  Paths change when another app mounts your package under a
# different api prefix, but the route name is stable.
#
# Every route is auto-named with your package's short name ('appstub').  Api
# routes also get an 'api' segment (from the name_prefix='api' default of
# register_http_api_routes() in your provider), so the welcome endpoint at
# GET /api/welcome is named 'appstub.api.welcome'.
# Tip: list every route's name + path with:  ./uvicore http routes
#
# To turn a route name into its URL FROM CODE, call url_path_for(name) on the
# built ASGI app (uvicore.app.http).  That's the very same Starlette name
# registry the Jinja `url()` template helper resolves against - so your tests
# and templates stay in sync with the real, prefix-aware paths.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_welcome_api_endpoint(client):
    # Resolve the route name to its path ('/api/welcome') - no hardcoded URL
    url = uvicore.app.http.url_path_for('appstub.api.welcome')

    res = await client.get(url)

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
