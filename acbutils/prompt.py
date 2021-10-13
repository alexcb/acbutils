def prompt(msg, default=None):
    yes = ("yes", "y")
    no = ("no", "n")

    if default is None:
        msg += " [yes/no]"
    elif default.lower() in yes:
        msg += " [Yes/no]"
    elif default.lower() in  no:
        msg += " [yes/No]"
    else:
        raise ValueError(default)

    while True:
        answer = input(msg)
        if answer == '' and default:
            answer = default
        if answer.lower() in yes:
            return True
        if answer.lower() in no:
            return False
