import pytest
import uvicore
from uvicore.support.dumper import dump, dd


# ------------------------------------------------------------------------------
# Example: the simplest possible test - does the app boot?
#
# Requesting the `app` fixture (defined in tests/conftest.py) bootstraps your
# entire Uvicore application: config merging, every provider's register()/boot(),
# and the IoC container.  If all of that succeeds, this test passes.  Use this as
# the template for plain (non-HTTP) unit tests of your services, models, etc.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_app_boots(app):
    # Once booted, the application singleton is available globally as uvicore.app
    assert uvicore.app is not None

    # And your package config is merged in and reachable by namespace
    assert uvicore.config('acme.appstub') is not None
