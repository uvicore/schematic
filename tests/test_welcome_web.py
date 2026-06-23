import pytest
import uvicore
from uvicore.support.dumper import dump, dd


# ------------------------------------------------------------------------------
# Example: testing a WEB route
#
# This hits the stock welcome page registered in http/routes/web.py, which
# includes the controller at http/controllers/welcome.py.  That controller
# serves GET '/' and renders the http/views/appstub/welcome.j2 template.
#
# Just like the api test, we reference the route by NAME instead of a hardcoded
# URL.  Web routes are auto-named with your package short name (no 'api'
# segment), so this page is named 'appstub.welcome'.  url_path_for(name) on the
# built app (uvicore.app.http) resolves it to its real path - the code-level
# equivalent of the Jinja `url()` helper.
# Tip: list every route's name + path with:  ./uvicore http routes
#
# The `client` fixture (tests/conftest.py) gives you an httpx AsyncClient wired
# straight to your ASGI app - no running server needed.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_welcome_web_page(client):
    # Resolve the route name to its path ('/') - no hardcoded URL
    url = uvicore.app.http.url_path_for('appstub.welcome')

    res = await client.get(url)

    # The page renders successfully...
    assert res.status_code == 200, res.text

    # ...as server-rendered HTML
    assert 'text/html' in res.headers['content-type']
