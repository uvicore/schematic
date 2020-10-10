import os
from lib.console import *

# Uvicore installer
# mReschke 2020-10-10

"""
NOTE to developers creating their own app schemas
Ensure this installer does not use any 3rd party modules, stdlib only.
"""

# header('header here')
# header('header here', GREEN, BLUE)
# log('log here')
# info('info here')
# line()
# line('#', PURPLE)
# item('item here')
# item('item here', '  +', RED, WHITE)
# message('message here')
# message('message here', 'LOOK AT ME', RED, YELLOW)
# info('MULTILINE:', PURPLE)
# info("""  new line message
#   asdfasdf
#   asdfasdf""")
# notice('notice here')
# warning('warning here')
# error('error here')

path = os.path.realpath(__file__ + '../../../')



header('Uvicore Installer Customizer')

info('PATH: ' + path)



