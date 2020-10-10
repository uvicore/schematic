from lib.console import *


def h1(log):
    header(log, "=", LIGHTGREEN, WHITE, 80)


def package_name():
    h1("Package Name")
    log("""Package name is the actual python package "namespace.name". Most uvicore
packages should be given a single namespace, preferably your name, developer
alias or company name.  Examples of what to enter here:""")
    item("mreschke.wiki")
    item("yourname.blog")
    item("companyname.themes")
    log("""Please do not skip the namespace and create root packages as they will
eventually cause namespace colissions amoung developers.""")
    nl()
    default = "acme.app"
    result = user_input("Package Name ({}): ".format(default))
    return result or default


def friendly_name():
    h1("Friendly Name")
    log("""asdfasdfasdf""")
    nl()
    default = "Acme Test App"
    result = user_input("Friendly Name ({}): ".format(default))
    return result or default
