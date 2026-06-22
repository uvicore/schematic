import pytest
import uvicore
import pytest_asyncio
from uvicore.support.dumper import dump, dd


# NOTE: pytest-asyncio 1.x removed support for overriding the `event_loop`
# fixture.  The single session-wide loop is now configured declaratively via
# [tool.pytest.ini_options] asyncio_default_{fixture,test}_loop_scope = "session"
# in pyproject.toml, so no custom event_loop fixture is needed (or allowed) here.


@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def appstub():

    # Setup Tests
    ############################################################################
    # Bootstrap uvicore application
    from acme.appstub.package import bootstrap
    app = bootstrap.Application(is_console=True)()

    # Register a PytestStartup event (uvicore.console.events.command.PytestStartup)
    # Which is listened to by database/db.py to connect to all dbs
    from uvicore.console.events import command as ConsoleEvents
    await ConsoleEvents.PytestStartup().codispatch()

    # Drop/Create and Seed Database
    # from uvicore.database.commands import db
    # await db.drop_tables('appstub')
    # await db.create_tables('appstub')
    # await db.seed_tables('appstub')

    # Run ALL Tests
    ############################################################################

    yield ''

    # Tear down tests
    ############################################################################
    #metadata.drop_all(engine)

    # Register a PytestShutdown event (uvicore.console.events.command.PytestShutdown) to disconnect from all DBs
    await ConsoleEvents.PytestShutdown().codispatch()


# Async HTTP test client (encode/httpx) bound directly to your ASGI app.
#
# Why this fixture has to "rebuild" the server:
# Under pytest the framework forces uvicore.app.is_http = False, so the normal
# HTTP bootstrap early-returns and never builds/mounts the web + api servers
# (uvicore.app.http stays None).  This fixture flips the app into HTTP mode,
# re-runs the HTTP bootstrap handler to actually build and mount the servers,
# then restores the original flags (the built server persists on
# uvicore.app.http).  It yields an httpx AsyncClient you can use to hit both
# your web routes (GET '/') and your api routes (GET '/api/welcome') end to end.
#
# Depends on `appstub` so the application is fully booted first.
@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def client(appstub):
    from httpx import ASGITransport, AsyncClient
    from uvicore.http.package.bootstrap import Http
    from uvicore.foundation.events.app import Booted

    # Save the original (pytest) flags
    orig_is_http = uvicore.app.is_http
    orig_is_console = uvicore.app.is_console

    # Flip into HTTP mode and (re)build the web + api servers
    uvicore.app._is_console = False
    uvicore.app._is_http = True
    Http()(Booted())

    # Restore the original flags; the built server remains attached to uvicore.app
    uvicore.app._is_http = orig_is_http
    uvicore.app._is_console = orig_is_console

    assert uvicore.app.http is not None, "HTTP server was not built for tests"

    async with AsyncClient(transport=ASGITransport(app=uvicore.app.http), base_url="http://testserver") as client:
        yield client
