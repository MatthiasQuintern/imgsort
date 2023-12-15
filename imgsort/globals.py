version = "1.2.1"
fullversion = f"{version}"

settings_map = {
            "q": "quit",
            "s": "skip",
            "u": "undo",
            "o": "open"
        }

from os import makedirs

def error(*args, exitcode=1, **kwargs):
    print("\033[31mError: \033[0m", *args, **kwargs)
    exit(exitcode)

def user_error(*args, **kwargs):
    print("\033[31mError: \033[0m", *args, **kwargs)

def warning(*args, **kwargs):
    print("\033[33mWarning: \033[0m", *args, **kwargs)

def info(*args, **kwargs):
    print("\033[34mInfo: \033[0m", *args, **kwargs)

def create_dir(d):
    try:
        makedirs(d)
    except PermissionError as e:
        error(f"Could not create '{d}': PermissionError: {e}")
    except Exception as e:
        error(f"Could not create '{d}': {e}")
