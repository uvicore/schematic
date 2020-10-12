import os
from lib.console import *
from lib import questions
from lib.install import install_now

"""
Uvicore installer
mReschke 2020-10-10

Note to schema designers and developers:
Ensure this installer does not use any 3rd party modules, stdlib only.
You can customize questions by adding new ones to install/questions.py
and firing them off in the answers{} below.  Be sure to customize the
install/install.py to handle the new answers properly.
"""

if __name__ == "__main__":
    # New packages full path
    path = os.path.realpath(__file__ + "../../../")

    # Ask questions and record answers
    # Schema designers can customze this section to ask more questions
    answers = {
        'path': path,
        'package_name': questions.package_name(),
        'friendly_name': questions.friendly_name(),
        'your_name': questions.your_name(),
        'your_email': questions.your_email(),
        'environment': questions.environment(),
    }

    # Confirm answers before install
    nl(2); line("#", LIGHTBLUE); nl(2)
    info("You are are about to customize this blank uvicore package schema as follows:")
    for answer in answers.items(): item(answer)
    nl(); go = user_confirm("Continue"); nl()

    # Install package with question answers
    if go: install_now(answers)

    # User cancelled, abort installation
    if not go:
        error("Installation aborted.")
        info("This package is in an error state and is not configured to actually run.")
        info("You can manually re-run:")
        info("  python ./.install/install.py", DARKGRAY)
        info("Or you can go ahead and delete this {}".format(path))
        info("folder and start over with the 'uvicore-new-app' command. Bye.")
        error("Installation aborted.")
