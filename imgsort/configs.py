from os import path, getcwd, listdir, mkdir, makedirs, rename
import re

def read_config(filepath, root_directory="."):
    if not path.isfile(filepath): return False

    file = open(filepath, 'r')
    keys = {}
    for line in file.readlines():
        line = line.replace("\n", "")
        match = re.match(r". = /?([a-z-A-ZöÖäÄüÜ0-9/: _-]+/)*[a-zA-ZöÖäÄüÜ0-9/: _-]+/?", line)
        if match:
            key, value = line.split(" = ")
            keys[key]  = root_directory + "/" + value
    return keys

def write_config(filepath, keys):
    file = open(filepath, 'w')
    file.write("Config written by imgsort.\n")
    for k, v in keys.items() :
        file.write(f"{k} = {v}\n")

def create_config():
    keys = {}
    print(
"""
===================================================================================================
Creating a new config
    Please enter at least one key and one directory.
    The key must be one single letter, a single digit number or some other keyboard key like .-#+&/ ...
    The key can not be 'q', 's', 'o' or 'u'.
    The directory must be a valid path to a directory, but is does not have to exist.
    You can use an absolute path (starting with '/', not '~') or a relative path (from here).
===================================================================================================
"""
            )

    done = False
    while not done:

        # ask for key
        key = input("Please enter a key or 'q' when you are done: ")
        if (len(key) != 1):
            print("Invalid key: " + key)
            continue
        # if done
        elif key == 'q':
            save = input("\nDo you want to save the config to ~/.config/imgsort/<name>.conf?\nType a name to save the config or type 'q' to not save the config: ")
            if not save == 'q':
                config_path = path.expanduser("~") + "/.config/imgsort"
                if not path.isdir(config_path):
                    mkdir(config_path)

                write_config(path.normpath(config_path + "/" + save + ".conf"), keys)
            done = True
            continue

        # ask for directory
        directory = input("Please enter the directory path: ")
        match = re.match(r"/?([a-z-A-ZöÖäÄüÜ0-9/: _\-]+/)*[a-z-A-ZöÖäÄüÜ0-9/: _\-]+/?", directory)
        if not match:
            print("Invalid directory path: " + directory)
            continue

        keys[key] = directory
        print(f"Added: ({key}: {directory})\n")

    return keys


def select_config():
    """
    Returns to path to an existing config or False if a new config should be created
    """
    # get configs
    config_path = path.expanduser("~") + "/.config/imgsort"
    if not path.isdir(config_path) or len(listdir(config_path)) == 0:
        return False

    configs = {}

    i = 1
    for file in listdir(config_path):
        if not re.match(r"[a-zA-ZöÖäÄüÜ0-9_\- ]+\.conf", file): continue

        configs[str(i)] = file
        i += 1

    # print configs
    print("0: Create new config")
    for n, conf in configs.items():
        print(f"{n}: {conf}")

    choice = input("Please select a config: ")
    if choice == "0": return None
    elif choice in configs:
        return path.normpath(config_path + "/" + configs[choice])
    else:
        print("Invalid choice - creating new config")
        return None
