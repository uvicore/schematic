# Bash colors
DEFAULT="\033[0;0m"
BLUE="\033[0;34m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
RED="\033[0;31m"
PURPLE="\033[0;35m"
BROWN="\033[0;33m"
LIGHTGRAY="\033[0;37m"
DARKGRAY="\033[1;30m"
LIGHTBLUE="\033[1;34m"
LIGHTGREEN="\033[1;32m"
LIGHTCYAN="\033[1;36m"
LIGHTRED="\033[1;31m"
LIGHTPURPLE="\033[1;35m"
YELLOW="\033[1;33m"
WHITE="\033[1;37m"

# Output helper methods
def header(o, c1=BROWN, c2=GREEN):
    print("{}:: {}{} {}::{}".format(c1, c2, o, c1, DEFAULT))

def log(o, c1=DEFAULT):
    print("{}{}{}".format(c1, o, DEFAULT))

def info(o, c1=WHITE):
    log(o, c1)

def line(l='-', c1=GREEN):
    print("{}{}{}".format(c1, l * 80, DEFAULT))

def item(o, b='  *', c1=BLUE, c2=DARKGRAY):
    print("{}{} {}{}{}".format(c1, b, c2, o, DEFAULT))

def message(o, w='MESSAGE', c1=BLUE, c2=WHITE):
    print("{}{}: {}{}{}".format(c1, w, c2, o, DEFAULT))

def notice(o, c1=PURPLE, c2=WHITE):
    message(o, 'NOTICE', c1, c2)

def warning(o, c1=YELLOW, c2=WHITE):
    message(o, 'WARNING', c1, c2)

def error(o, c1=LIGHTRED, c2=RED):
    message(o, 'ERROR', c1, c2)
