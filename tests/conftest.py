import pytest
import asyncio
import uvicore
import pytest_asyncio
from uvicore.support.dumper import dump, dd


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def appstub(event_loop):

    # Setup Tests
    ############################################################################
    # Bootstrap uvicore application
    from acme.appstub.package import bootstrap
    app = bootstrap.Application(is_console=True)()

    # Register a PytestStartup event (uvicore.console.events.command.PytestStartup)
    # Which is listened to by database/db.py to connect to all dbs
    from uvicore.console.events import command as ConsoleEvents
    await ConsoleEvents.PytestStartup().codispatch()

    # Drop/Create and Seed SQLite In-Memory Database
    # from acme.appstub.database.seeders import seed
    # engine = uvicore.db.engine()
    # metadata = uvicore.db.metadata()
    # metadata.drop_all(engine)
    # metadata.create_all(engine)
    # await seed()


    # Run ALL Tests
    ############################################################################

    yield ''

    # Tear down tests
    ############################################################################
    #metadata.drop_all(engine)

    # Register a PytestShutdown event (uvicore.console.events.command.PytestShutdown) to disconnect from all DBs
    await ConsoleEvents.PytestShutdown().codispatch()
