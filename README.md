# Uvicore App Stub

This repository is used by the uvicore installer tool when creating a new uvicore application/package.


# Bugs

During installer a ' in app name causes the app.py config to error.  Need to trim all invalid characters.

no vendor in package, just a name, makes wrong dir, it double does the vendor as the package name.  creating ./myapp/myapp still, should be just ./myapp if no vendor

OR just force the installer to require a vendor.package style
Though not sure how it would handle multiple.vendor.name.things


maybe a note when done stating they have to install their own env



# Below is JUNK NOTES to remove


# Questions to Ask

I need these questions so I can stub out certain things

friendly name: Matts Wiki
package name: mreschke.wiki
your name: Matthew Reschke
Your email: mail@example.com
Type of environment:
    Poetry
    Pipenv
    requirements.txt



# On install

Don't assume poetry, but my working app stub will use poetry

delete poetry.lock, pyproject.toml

They can pick which venv, virtualenv, poetry or pipenv and I have to create stubs for those.
Maybe include folders with those stubs, then replace files and delete other stubs
Maybe a .stubs directory that is deleted after all is installed.
Or a .install directory which has the install script and all stubs, and deletes itself


Maybe DONT install anything, just make a pyenv or poetry file, they have to make their ENV and install themselves.




Don't assume python version

delete .python-version


README

Set readme properly.  Remember to add how to serve manually with gunicorn and uvicorn.



# Installer Ideas

global

Default
uvicore-install app --name=mreschke.wiki --path=./wiki --repo=https://github.com/uvicore.app --branch=something --tag=something

Override repo and branch OR tag
puvicore-install app --name=mreschke.wiki --path=./wiki --repo=https://github.com/uvicore.app --branch=something --tag=something
