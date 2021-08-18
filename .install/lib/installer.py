import os
import shutil
import fileinput
from os.path import realpath
from lib.console import *
from lib import helpers
from pathlib import Path
from datetime import datetime


class Installer:

    def __init__(self, options, version):
        # Extract options for easier access
        self.options = options
        self.path = options.get("path")
        self.package = options.get("package_name")
        self.friendly_name = options.get("friendly_name")
        self.your_name = options.get("your_name")
        self.your_email = options.get("your_email")
        self.env = options.get("environment").lower()
        self.version = version

        # Derived options
        self.vendor = self.package.split(".")[0]
        self.app = self.package.split(".")[-1]
        self.stubs = realpath(self.path + "/.install/stubs")

        # Replacements (order is important)
        self.replacements = [
            ("acme-appstub", self.package.replace(".", "-").replace("_", "-")),
            ("acme.appstub", self.package),
            ("acme/appstub", self.package.replace(".", "/")),
            ("acme", self.vendor),
            ("appstub", self.app),
            ("Appstub", helpers.studly(self.app)),
            ("APPSTUB", self.app.upper()),
            ("Acme Test App", self.friendly_name),
            ("Artisan Smith", self.your_name),
            ("<smith@example.com>", "<" + self.your_email + ">"),
            ("<year>", str(datetime.now().year)),
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

        # Move package
        self.move_package()

        # Cleanup
        self.cleanup()

        # Done
        self.done()

    def delete_test_files(self):
        nl(); header("Deleting unused test files and folders")
        self.delete([
            ".git",
            ".env",
            ".coverage",
            "poetry.lock",
            "pyproject.toml",
            ".python-version",
            ".vscode",
        ])

    def copy_stubs(self):
        nl(); header("Copying stubbed files")

        # Copy virtual environment file
        if self.env == "poetry":
            self.copy([(".install/stubs/pyproject.toml", "pyproject.toml")])
        elif self.env == "pipenv":
            self.copy([(".install/stubs/Pipfile", "Pipfile")])
        elif self.env == "requirements.txt":
            self.copy([(".install/stubs/requirements.txt", "requirements.txt")])

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
        self.replace([
            "uvicore",
            ".env-example",
            "LICENSE",
        ])
        if self.env == "poetry": self.replace(["pyproject.toml"])

    def rename_files(self):
        nl(); header("Renaming files to new package name")
        self.rename([
            ("acme/appstub/config/appstub.py", "acme/appstub/config/" + self.app.lower() + ".py"),
            ("acme/appstub/http/views/appstub", "acme/appstub/http/views/" + self.app.lower()),
            ("acme/appstub/services/appstub.py", "acme/appstub/services/" + self.app.lower() + ".py"),
        ])

        # Copy (not rename) .env-example to .env
        self.copy([(".env-example", ".env")])

        # Detect if vendor=uvicore, if so, have to rename our uvicore script to uvicore-cli
        if (self.vendor.lower() == 'uvicore'):
            self.rename([('uvicore', 'uvicore-cli')])

    def move_package(self):
        nl(); header("Moving package folder to new package name")
        paths = self.package.split(".")
        full_path = ''
        for path in paths:
            full_path += "/" + path
            os.mkdir(self.path + full_path)
        self.rename([("acme/appstub", self.package.replace('.', '/'))])

    def cleanup(self):
        nl(); header("Cleaning up")
        self.delete([
            "acme",
            ".install",
        ])

    def done(self):
        nl(2); line("#", LIGHTBLUE); nl(2)
        #info("Uvicore installer complete!  You must now MANUALLY:", BROWN)
        header("Uvicore installation complete!  You must now MANUALLY perform the following:", h="!!", c1=RED, c2=BROWN)

        item("cd {}".format(self.path), c2=WHITE)

        # Poetry
        if self.env == "poetry":
            item("poetry shell", c2=WHITE)
            item("poetry install", c2=WHITE)
            #info("    [OPTIONAL] If you need database and/or web and api support run: poetry add uvicore[database,web]", CYAN)

        if self.env == "pipenv":
            item("pipenv shell", c2=WHITE)
            item("pipenv install", c2=WHITE)
            #info("    [OPTIONAL] If you need database and/or web and api support run: pipenv install uvicore[database,web]=={}.*".format(self.version), CYAN)
            #pipenv install uvicore[database,web]==0.1.*

        if self.env == "requirements.txt":
            item("python -m venv env", c2=WHITE)
            item("source ./env/bin/activate", c2=WHITE)
            #info("    [OPTIONAL] If you need database and/or web and api support edit requirements.txt like so: uvicore[database,web] == {}.*".format(self.version), CYAN)
            item("pip install -r requirements.txt", c2=WHITE)

        #item("Initialize your preferred environment (venv, virtualenv, pyenv, poetry...)")
        #item("If you will be using a database (MySQL, Postgres or SQLite) install uvicore[database] extras")
        #item("If you will be using web and api install uvicore[web] extras")
        #item("Install dependencies in your environment provided by the uvicore installer")

        item("Modify the LICENSE file to your liking", c2=WHITE)
        if self.env == "poetry": item("Modify the license listed in your pyproject.toml file", c2=WHITE)
        item("Modify .gitignore and .editorconfig to your liking", c2=WHITE)
        item("Add code to git or other source control provider", c2=WHITE)
        item("Run ./uvicore", c2=WHITE)
        item("Run ./uvicore {} welcome".format(self.app), c2=WHITE)
        item("Run ./uvicore http serve", c2=WHITE)
        item("Visit http://127.0.0.1:5000", c2=WHITE)
        item("Visit http://127.0.0.1:5000/api/docs", c2=WHITE)

        nl();
        info("Thanks for using Uvicore!", LIGHTBLUE)


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

