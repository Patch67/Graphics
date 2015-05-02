def get_line(f):
    __line = f.readline().rstrip()
    while __line == "":  # skip over empty lines
        __line = f.readline().rstrip()
    return __line


def check_line(l, expected):
    __line = l.rstrip()
    if __line == expected:
        return True
    else:
        print("Error '%s' found but expected '%s'" % (expected, __line))
        return False


def process_menu(file):
    __line = get_line(file)
    while __line[0] == "-":
        if __line[1:] != "":
            print("-Submenu %s" % __line[1:])
        else:
            print("--Spacer--")
        __line = get_line(file)
    return __line


def process_keys(file):
    __line = get_line(file)
    while __line != "Toolbars":
        print("Keys %s" % __line)
        __line = get_line(file)
    return __line


def process_toolbars(file):
    __line = get_line(file)
    while __line != "End":
        print("Toolbar is %s" % __line)
        __line = get_line(file)
        while __line[0] == "-":
            print("-Tool is %s" % __line[1:])
            __line = get_line(file)
        __line = get_line(file)

file = open("gui.conf", "r")
if check_line(get_line(file), "Application"):
    line = get_line(file)
    print("Application name is %s" % line)
    if check_line(get_line(file), "Menus"):
        line = get_line(file)
        print("Menu is % s" % line)
        line = process_menu(file)
        while line != "Keys":
            print("Menu is % s" % line)
            line = process_menu(file)
        if check_line(line, "Keys"):
            print("Keys")
            line = process_keys(file)
        if check_line(line, "Toolbars"):
            print("Toolbars")
            process_toolbars(file)

file.close()