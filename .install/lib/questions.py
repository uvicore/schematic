from lib.console import *
from collections import OrderedDict

def h1(log):
    header(log, "=", LIGHTGREEN, WHITE, 80)


def package_name(default):
    nl(2); h1("Package Name")
    log("""Package name is the actual "python package" compatible name. Most uvicore
packages should be given a vendor.package style namespace, preferably your name, developer
alias or company name.  Examples of what to enter here:""")
    item("mreschke.wiki")
    item("yourname.blog")
    item("companyname.themes")
    log("""Please do not skip the namespace and create root packages as they will
eventually cause namespace collisions amoung developers.""")
    nl()
    result = user_input("Package Name ({}): ".format(default))

    # NO
    # good = False
    # while not good:
    #     result = user_input("Package Name ({}): ".format(default))
    #     # Check for reserved package names
    #     name = result.split(".")[-1]
    #     exclude = ["config", "event", "gen", "ioc", "package"]
    #     if name in exclude:
    #         error("Package name cannot be one of {}".format(exclude))
    #     else:
    #         good = True
    return result or default


def friendly_name(default):
    nl(2); h1("Friendly Name")
    log("""Friendly name of this package, for example: Wiki, Acme Blog, Reporting Suite...""")
    nl()
    result = user_input("Friendly Name ({}): ".format(default))
    return result or default


def your_name(default):
    nl(2); h1("Your Name")
    log("""Your full name is used in one of poetry pyproject.toml, setup.py or other
config type files.""")
    nl()
    result = user_input("Your Full Name ({}): ".format(default))
    return result or default


def your_email(default):
    nl(2); h1("Your Email")
    log("""Your email is used in one of poetry pyproject.toml, setup.py or other
config type files.""")
    nl()
    result = user_input("Your Email ({}): ".format(default))
    return result or default


def environment(default):
    nl(2); h1("Preferred Environment")
    log("""There are many python virtual environments people prefer.  This installer
will create the proper FILES (pyproject.toml, Pipfile, requirements.txt...) for
you but it will NOT actually create or activate any environments nor will it
install any package dependencies.  The installer will leave that up to you.""")
    nl()
    options = OrderedDict({
        "Poetry": "Creates a pyproject.toml poetry file",
        "Pipenv": "Creates a Pipfile pipenv file",
        "Requirements.txt": "Creates a simple requirements.txt file",
    })
    return user_select("Virtual Environment ({}): ", options, default)
