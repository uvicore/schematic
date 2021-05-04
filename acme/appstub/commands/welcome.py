import uvicore
from uvicore.console import command
from uvicore.support.dumper import dump, dd


@command()
async def cli():
    """Welcome to Uvicore"""

    print("""Welcome to a Uvicore Example CLI Command!

This command lives in your commands/welcome.py file and is registered with the CLI
in your services/appstub.py boot() method.  Create as many CLI commands as needed
and be sure to checkout the commands included with the uvicore packages.

~mReschke""")
