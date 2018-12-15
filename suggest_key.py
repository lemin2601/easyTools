try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")


commands = [
    'here@blubb.com',
    'foo@bar.com',
    'whatever@wherever.org',
]


def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)


def main():

    while 1:
        a = input("> ")
        print("You entered", a)


if __name__ == "__main__":
    main()
