from getpass import getpass
import os


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


def cmd_output_to_file(node_dir, filename, content):
    full_file_path = os.path.join(node_dir, filename)
    with open(full_file_path, 'w') as out_file:
        out_file.write(content + '\n')


def command_to_filename(cmd):
    return cmd.rstrip().replace(' ', '_') + '.txt'
