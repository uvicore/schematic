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
        self.extra_db = options.get('extra_db')
        self.extra_redis = options.get('extra_redis')
        self.extra_web = options.get('extra_web')
        self.extra_themes = options.get('extra_themes')
        self.env = options.get("environment").lower()
        self.version = version

        # Derived options
        self.vendor = self.package.split(".")[0]
        self.app = self.package.split(".")[-1]
        self.stubs = realpath(self.path + "/.install/stubs")

        # Replacements (order is important)
        self.replacements = [
            # These are complex replacements build from the "extras" chosen during install
            # Must be first as complex output even uses acme-appstub, which should be later merged
            ("<package-dependencies>", self.template_package_dependencies()),
            ("<provider-imports>", self.template_provider_imports()),
            ("<provider-class>", self.template_provider_class()),
            ("<provider-db-connections>", self.template_provider_db_connections()),
            ("<pyproject-uvicore>", self.template_pyproject_uvicore()),
            ("<pipfile-uvicore>", self.template_pipfile_uvicore()),
            ("<requirements-uvicore>", self.template_requirements_uvicore()),

            # Comment things based on extras
            ("self.register_views()", 'self.register_views()' if self.extra_web else '#self.register_views()'),
            ("self.register_routes()", 'self.register_routes()' if self.extra_web else '#self.register_routes()'),

            # Basic replacements
            ("acme-appstub", self.package.replace(".", "-").replace("_", "-")),
            ("acme.appstub", self.package),
            ("acme/appstub", self.package.replace(".", "/")),
            ("acme", self.vendor),
            ("appstub", self.app),
            ("Appstub", helpers.studly(self.app)),
            ("APPSTUB", self.app.upper()),
            ("Acme Test App", self.friendly_name),
            ("Artisan Smith", self.your_name),
            ("smith@example.com", self.your_email),
            ("<year>", str(datetime.now().year))
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

        # Copy readme
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
            "serve-gunicorn",
            "serve-uvicorn",
            "README.md",
            "acme/appstub/http/views/appstub/welcome.j2",
        ])
        if self.env == "poetry": self.replace(["pyproject.toml"])

    def rename_files(self):
        nl(); header("Renaming files to new package name")
        self.rename([
            ("acme/appstub/config/appstub.py", "acme/appstub/config/" + self.app.lower() + ".py"),
            ("acme/appstub/http/views/appstub", "acme/appstub/http/views/" + self.app.lower()),
            ("acme/appstub/http/public/assets/appstub", "acme/appstub/http/public/assets/" + self.app.lower()),
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
            if not os.path.exists(self.path + full_path):
                os.mkdir(self.path + full_path)
        self.rename([("acme/appstub", self.package.replace('.', '/'))])

    def cleanup(self):
        nl(); header("Cleaning up")
        self.delete([".install"])
        if self.vendor != 'acme': self.delete(["acme"])

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


    ############################################################################
    ############################################################################
    ############################################################################


    def template_provider_db_connections(self):
        results = ""

        if self.extra_redis: results += """
        # Define Redis Connections
        self.register_redis_connections(
            connections=self.package.config.redis.connections,
            default=self.package.config.redis.default
        )
"""

        if self.extra_db: results += """
        # Define Database Connections
        self.register_db_connections(
            connections=self.package.config.database.connections,
            default=self.package.config.database.default
        )

        # Define all tables, models and seeders
        # Order does not matter as they are sorted topologically for ForeignKey dependencies
        # If you don't have an __init__.py index in your tables or models you can use
        # wildcard imports self.register_db_models(['acme.appstub.models.*])
        self.register_db_models([
            'acme.appstub.models',
        ])
        self.register_db_tables([
            'acme.appstub.database.tables',
        ])
        self.register_db_seeders([
            'acme.appstub.database.seeders.seed',
        ])
"""
        return results

    def template_provider_class(self):
        results = ""
        if (self.extra_redis): results += ", Redis"
        if (self.extra_db): results += ", Db"
        if (self.extra_web): results += ", Http"
        return results

    def template_provider_imports(self):
        results = ""
        if (self.extra_web): results += "from uvicore.http.package.registers import Http\n"
        if (self.extra_redis): results += "from uvicore.redis.package.registers import Redis\n"
        if (self.extra_db): results += "from uvicore.database.package.registers import Db\n"
        return results

    def template_package_dependencies(self):
        results = ""
        if (self.extra_redis):
            results += """
    # Redis provides redis access and redis caching if enabled in your app config
    'uvicore.redis': {
        'provider': 'uvicore.redis.package.provider.Redis',
    },
"""
        if (self.extra_db):
            results += """
    # Database is required for database queries and the ORM.  Disable if your project
    # does not require database or models
    'uvicore.database': {
        'provider': 'uvicore.database.package.provider.Database',
    },

    # ORM provides an object relationional mapper between your databse tables
    # and your ORM models.  Disable if your project does not require Models.
    # Even without the ORM, you can still use the database with the db query builder.
    'uvicore.orm': {
        'provider': 'uvicore.orm.package.provider.Orm',
    },
"""

        if (self.extra_web):
            results += """
    # Auth provides all of the auth middleware, user providers, authenticators and guards
    # 'uvicore.auth': {
    #     'provider': 'uvicore.auth.package.provider.Auth',
    # },

    # Templating engine for HTTP Web Routes
    'uvicore.templating': {
        'provider': 'uvicore.templating.package.provider.Templating',
    },

    # HTTP provides API and WEB endpoints, assets, templates.  A full webserver.
    'uvicore.http': {
        'provider': 'uvicore.http.package.provider.Http',
    },
"""
        return results

    def template_pyproject_uvicore(self):
        # Poetry 1.0 style using [tool.poetry.dependencies] section
        results = 'uvicore = {version = "0.3.*"'
        extra = []
        if (self.extra_db): extra.append("database")
        if (self.extra_redis): extra.append("redis")
        if (self.extra_web): extra.append("web")
        if (self.extra_themes): extra.append("themes")
        if extra:
            results += ', extras = ["' + '", "'.join(extra) + '"]'
        else:
            results += ', extras = []'
        results += "}"
        return results

        # Poetry 2.0 style using dependencies = [] section
        # Downside of this is you can't specify path develop-true deps
        # I will keep using 1.0 style (which works in 2.0) until it's deprecated by poetry
        # results = '    "uvicore'
        # extra = []
        # if (self.extra_db): extra.append("database")
        # if (self.extra_redis): extra.append("redis")
        # if (self.extra_web): extra.append("web")
        # if (self.extra_themes): extra.append("themes")
        # if extra:
        #     results += '["' + '","'.join(extra) + '"]'
        # results += '==0.3.*"'
        # return results

    def template_pipfile_uvicore(self):
        results = 'uvicore = {version = "==0.3.*"'
        extra = []
        if (self.extra_db): extra.append("database")
        if (self.extra_redis): extra.append("redis")
        if (self.extra_web): extra.append("web")
        if (self.extra_themes): extra.append("themes")
        if extra:
            results += ', extras = ["' + '", "'.join(extra) + '"]'
        else:
            results += ', extras = []'
        results += "}"
        return results

    def template_requirements_uvicore(self):
        results = 'uvicore'
        extra = []
        if (self.extra_db): extra.append("database")
        if (self.extra_redis): extra.append("redis")
        if (self.extra_web): extra.append("web")
        if (self.extra_themes): extra.append("themes")
        if extra:
            results += '["' + '", "'.join(extra) + '"]'
        results += ' == 0.3.*'
        return results
