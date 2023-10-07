import uvicore
from uvicore.support.dumper import dump, dd
from uvicore.exceptions import SmartException
from uvicore.console import command, argument, option


@command()
async def cli():
    """Welcome to Uvicore"""
    try:

        print("""Welcome to a Uvicore Example CLI Command!

This command lives in your commands/welcome.py file and is registered with the CLI
in your package/provider.py boot() method.  Create as many CLI commands as needed
and be sure to checkout the commands included with the uvicore packages.

~mReschke""")

    except SmartException as e:
        # Python exit() with any value means "error" in bash exit code speak!
        exit(e.detail)



# --------------------------------------------------------------------------
# Example: Command with arguments and options
# --------------------------------------------------------------------------
# @command(help="This is another place to set command help messages")
# @argument('id_or_name')
# @option('--tenant', help='Tenant')
# @option('--coin', default='BTC', help='Coin with Default')
# @option('--json', is_flag=True, help='Output results as JSON')
# async def get(id_or_name: str, tenant: str, coin: str, json: bool):
#     """This shows up as the commands help message"""
#     # ex: ./uvicore cmdname namearg --tenant bob --json
#     try:
#         # Do stuff
#         pass
#     except SmartException as e:
#         # Python exit() with any value means "error" in bash exit code speak!
#         exit(e.detail)
