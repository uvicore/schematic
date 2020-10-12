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
def header(o, h="::", c1=BROWN, c2=GREEN, l=None):
    if l:
        dash = round((l - (len(o) + 2)) / 2)
        # Max length for padding
        print("{}{} {}{} {}{}{}".format(c1, h * dash, c2, o, c1, h * dash, DEFAULT))
    else:
        print("{}{} {}{} {}{}{}".format(c1, h, c2, o, c1, h, DEFAULT))

def log(o="", c1=DEFAULT):
    print("{}{}{}".format(c1, o, DEFAULT))

def info(o, c1=WHITE):
    log(o, c1)

def line(l="-", c1=GREEN, s=80):
    print("{}{}{}".format(c1, l * s, DEFAULT))

def nl(c=1):
    for x in range(0, c): print()

def item(o, b="  *", c1=BLUE, c2=DARKGRAY):
    print("{}{} {}{}{}".format(c1, b, c2, o, DEFAULT))

def message(o, w="MESSAGE", c1=BLUE, c2=WHITE):
    print("{}{}: {}{}{}".format(c1, w, c2, o, DEFAULT))

def notice(o, c1=PURPLE, c2=WHITE):
    message(o, "NOTICE", c1, c2)

def warning(o, c1=YELLOW, c2=WHITE):
    message(o, "WARNING", c1, c2)

def error(o, c1=LIGHTRED, c2=RED):
    message(o, "ERROR", c1, c2)

def user_input(o, c1=WHITE):
    return input("{}{}{}".format(c1, o, DEFAULT))

def user_confirm(o, c1=WHITE):
    result = None
    while result != 'y' and result != 'n':
        result = input("{}{} (y/n)? {}".format(c1, o, DEFAULT)).lower()
    if result == 'y': return True
    return False

def user_select(o, selections, default, c1=BLUE, c2=WHITE):
    i = 1
    default_int = 0
    for k,v in selections.items():
        if default == k: default_int = i
        item(str(k) + ' - ' + str(v), str(i) + ") ", c1, c2)
        i += 1
    nl()
    result = 0
    while result < 1 or result > len(selections):
        result = user_input(o.format(default_int)) or default_int
        result = int(result)
    return list(selections.keys())[result - 1]
