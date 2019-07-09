from getpass import getpass


def get_credentials():
    """Prompts for, and returns, a username and a password."""
    user = input("Login: ")
    pwd = None
    while not pwd:
        pwd = getpass()
        pwd_verify = getpass('Re-enter password: ')
        if pwd != pwd_verify:
            print("Passwords do not match. Try again.")
            pwd = None
    return user, pwd


def command_to_filename(cmd):
    return cmd.rstrip().replace(' ', '_') + '.txt'
