from lib.console import *

def install_now(options):
    # Extract options for easier access
    path = options.get('path')
    package = options.get('package_name')
    name = options.get('friendly_name')


    header("Customizing Package Now")

    item(path)
    item(package)
    item(name)
