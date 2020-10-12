#import typer
import uvicore
from typing import List
from uvicore.console import command
from uvicore.support.dumper import dump, dd

@command()
async def cli():
    """Welcome to Uvicore"""

    print('Welcome to Uvicore Command Line Applications!')
