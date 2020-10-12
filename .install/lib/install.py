from lib.console import *

def install_now(options):
    # Extract options for easier access
    path = options.get('path')
    package_name = options.get('package_name')
    friendly_name = options.get('friendly_name')
    your_name = options.get('your_name')
    your_email = options.get('your_email')
    env = options.get('environment')


    header("Customizing Package Now")

    print(options)
