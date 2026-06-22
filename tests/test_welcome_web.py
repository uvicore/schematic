import pytest
import uvicore
from uvicore.support.dumper import dump, dd


# ------------------------------------------------------------------------------
# Example: testing a WEB route
#
# This hits the stock welcome page registered in http/routes/web.py, which
# includes the controller at http/controllers/welcome.py.  That controller
# serves GET '/' and renders the http/views/appstub/welcome.j2 template.
# (The leading path is your config/http.py web 'prefix', which defaults to '').
#
# The `client` fixture (tests/conftest.py) gives you an httpx AsyncClient wired
# straight to your ASGI app - no running server needed.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_welcome_web_page(client):
    res = await client.get('/')

    # The page renders successfully...
    assert res.status_code == 200, res.text

    # ...as server-rendered HTML
    assert 'text/html' in res.headers['content-type']
