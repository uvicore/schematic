import os
from lib.console import *
from lib import questions

"""
Uvicore installer
mReschke 2020-10-10

NOTE to developers creating their own app schemas
Ensure this installer does not use any 3rd party modules, stdlib only.
"""

if __name__ == "__main__":
    # New packages full path
    path = os.path.realpath(__file__ + "../../../")

    # Ask questions
    package = questions.package_name(); nl(2)
    name = questions.friendly_name(); nl(2)

    # Confirm answers
    line("#", LIGHTBLUE); nl()
    info("You are are about to customize this blank uvicore package schema as follows:")
    item("Path: " + path)
    item("Package Name: " + package)
    item("Friendly Name: " + name)
    nl()
    go = user_confirm("Continue")
    nl()

    # Install package or abort
    if go:
        install_now()
    else:
        error("Installation aborted.")
        info("This package is in an error state and is not configured to actually run.")
        info("You can manually re-run:")
        info("  python ./.install/install.py", DARKGRAY)
        info("Or you can go ahead and delete this {}".format(path))
        info("folder and start over with the 'uvicore-new-app' command. Bye.")
        error("Installation aborted.")






