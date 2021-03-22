import os
import shutil
import fileinput
from os.path import realpath
from lib.console import *
from lib import helpers
from pathlib import Path

class Installer:

    def __init__(self, options):
        # Extract options for easier access
        self.options = options
        self.path = options.get("path")
        self.package = options.get("package_name")
        self.friendly_name = options.get("friendly_name")
        self.your_name = options.get("your_name")
        self.your_email = options.get("your_email")
        self.env = options.get("environment").lower()

        # Derived options
        self.vendor = self.package.split(".")[0]
        self.app = self.package.split(".")[-1]
        self.stubs = realpath(self.path + "/.install/stubs")

        # Replacements (order is important)
        self.replacements = [
            ("acme-appstub", self.package.replace(".", "-").replace("_", "-")),
            ("acme.appstub", self.package),
            ("appstub", self.app),
            ("Appstub", helpers.studly(self.app)),
            ("APPSTUB", self.app.upper()),
            ("Acme Test App", self.friendly_name),
            ("Artisan Smith", self.your_name),
            ("<smith@example.com>", "<" + self.your_email + ">"),
        ]

    def handle(self):
        # Delete test files
        self.delete_test_files()

        # Copy stubbed files
        self.copy_stubs()

        # Search and replace files
        self.replace_all()

        # Rename files
        self.rename_files()

        # Cleanup
        self.cleanup()

        # Done
        self.done()

    def delete_test_files(self):
        nl(); header("Deleting unused test files and folders")
        self.delete([
            ".git",
            ".env",
            "poetry.lock",
            "/pyproject.toml",
            "/.python-version",
            "/.vscode",
        ])

    def copy_stubs(self):
        nl(); header("Copying stubed files")

        if self.env == "poetry":
            self.copy([
                (".install/stubs/pyproject.toml", "pyproject.toml"),
            ])

        self.copy([
            (".install/stubs/README.md", "README.md")
        ])

    def replace_all(self):
        nl(); header("Searching and Replacing acme.appstub in all files")

        # Find all python files
        ignores= [
            "/.install/"
        ]
        files = []
        for path in Path(self.path).rglob("*.py"):
            skip = False
            for ignore in ignores:
                if ignore in str(path):
                    skip = True
                    break
            if not skip:
                files.append(str(path)[len(self.path):])

        # Replace all python files
        self.replace(files)

        # Replace additional files
        if self.env == "poetry":
            self.replace([
                "uvicore",
                "pyproject.toml",
                ".env-example",
            ])

    def rename_files(self):
        self.rename([
            ("acme/appstub/config/appstub.py", "acme/appstub/config/" + self.app.lower() + ".py"),
            ("acme/appstub/http/views/appstub", "acme/appstub/http/views/" + self.app.lower()),
            ("acme/appstub/services/appstub.py", "acme/appstub/services/" + self.app.lower() + ".py"),

            # Env
            (".env-example", ".env"),

            # These must be last
            ("acme/appstub", "acme/" + self.app.lower()),
            ("acme", self.vendor.lower()),
        ])

    def cleanup(self):
        self.delete([
            '.install'
        ])

    def done(self):
        nl();
        info('Uvicore installer complete!  You must now MANUALLY:')
        item('cd {}'.format(self.path))
        item('Initialize your preferred environment (venv, virtualenv, pyenv, poetry...)')
        item('Install dependencies in your environment provided by the uvicore installer')
        item('Run ./uvicore')

    ############################################################################
    ############################################################################
    ############################################################################

    def delete(self, files):
        for filename in files:
            file = realpath(self.path + "/" + filename)
            if os.path.exists(file):
                item("Deleting {}".format(filename))
                if os.path.isdir(file):
                    shutil.rmtree(file)
                else:
                    os.remove(file)

    def copy(self, files):
        for file in files:
            src = realpath(self.path + "/" + file[0])
            dest = realpath(self.path + "/" + file[1])
            if os.path.exists(src):
                item("Copying {} to {}".format(file[0], file[1]))
                shutil.copyfile(src, dest)

    def replace(self, files):
        for filename in files:
            file = realpath(self.path + "/" + filename)
            if os.path.exists(file):
                item("Search and Replace in {}".format(filename))
                with fileinput.FileInput(file, inplace=True) as f:
                    for line in f:
                        for replacement in self.replacements:
                            line = line.replace(replacement[0], replacement[1])
                        print(line, end="")

    def rename(self, files):
        for file in files:
            src = realpath(self.path + "/" + file[0])
            dest = realpath(self.path + "/" + file[1])
            if os.path.exists(src):
                item("Renaming {} to {}".format(file[0], file[1]))
                os.rename(src, dest)

