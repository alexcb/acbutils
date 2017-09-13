def prompt(msg):
    while True:
        answer = raw_input("%s [yes/no]" % msg)
        if answer.lower() in ("yes", "y"):
            return True
        if answer.lower() in ("no", "n"):
            return False

