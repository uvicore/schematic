import uvicore
from uvicore.support import path
from uvicore.configuration import Env
from uvicore.support.dumper import dd, dump


class Application:
    """Bootstrap the application either from the CLI or Web entry points

    Bootstrap only runs when this package is running as the main app via
    ./uvicore or uvicorn/gunicorn server"""

    def __init__(self, is_console: bool = False):
        self.is_console = is_console

    def __call__(self):
        # Base path
        base_path = path.find_base(__file__)

        # Load .env from environs
        Env().read_env(base_path + '/.env')

        # Import this apps config (import must be after Env())
        from ..config.app import config as app_config

        # Bootstrap the Uvicore Application (Either CLI or HTTP entry points based on is_console)
        uvicore.bootstrap(app_config, base_path, self.is_console)

        # Return application
        return uvicore.app
