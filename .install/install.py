import os
from lib.console import *
from lib import questions
from lib.installer import Installer

"""
Uvicore installer
mReschke 2020-10-10

Note to schema designers and developers:
Ensure this installer does not use any 3rd party modules, stdlib only.
You can customize questions by adding new ones to lib/questions.py
and firing them off in the answers{} below.  Be sure to customize the
lib/installer.py to handle the new answers properly.
"""

# Test run over and over!
# rsync -vaP --delete /home/mreschke/Code/mreschke/python/uvicore/app/ . && python .install/install.py


if __name__ == "__main__":
    # New packages full path
    path = os.path.realpath(__file__ + "../../../")

    # Ask questions and record answers
    # Schema designers can customze this section to ask more questions
    # answers = {
    #     'path': path,
    #     'package_name': questions.package_name(default='acme.appstub'),
    #     'friendly_name': questions.friendly_name(default="Acme Test App"),
    #     'your_name': questions.your_name(default="Artisan Smith"),
    #     'your_email': questions.your_email(default="smith@example.com"),
    #     'environment': questions.environment(default='Poetry'),
    # }
    answers = {
        'path': path,
        'package_name': questions.package_name(default='mreschke.wiki'),
        'friendly_name': questions.friendly_name(default="mReschke Wiki"),
        'your_name': questions.your_name(default="Matthew Reschke"),
        'your_email': questions.your_email(default="mreschke@example.com"),
        'environment': questions.environment(default='Poetry'),
    }

    # Confirm answers before install
    nl(2); line("#", LIGHTBLUE); nl(2)
    info("You are are about to customize this blank uvicore package schema as follows:")
    for answer in answers.items(): item(answer)
    nl(); go = user_confirm("Continue"); nl()

    # Install package with question answers
    if go:
        installer = Installer(answers)
        installer.handle()

    # User cancelled, abort installation
    if not go:
        error("Installation aborted.")
        info("This package is in an error state and is not configured to actually run.")
        info("You can manually re-run:")
        info("  python ./.install/install.py", DARKGRAY)
        info("Or you can go ahead and delete this {}".format(path))
        info("folder and start over with the 'uvicore-new-app' command. Bye.")
        error("Installation aborted.")
