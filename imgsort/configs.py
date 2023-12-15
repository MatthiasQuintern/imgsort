import enum
from os import EX_CANTCREAT, path, getcwd, listdir, rename
from sys import exit
import re

from .globals import version, settings_map
from .globals import warning, error, user_error, info, create_dir

class ConfigManager():
    """Manage config files for imgsort"""
    def __init__(self, config_dir: str):
        """TODO: to be defined.

        @param config_path TODO

        """
        self._config_dir = config_dir
        if not path.isdir(self._config_dir):
            if path.exists(self._config_dir):
                error(f"Config '{self._config_dir}' exists but is not a directory.")
            info(f"Creating config dir '{self._config_dir}' since it does not exist")
            try:
                create_dir(self._config_dir)
            except PermissionError as e:
                error(f"Could not create '{self._config_dir}': PermissionError: {e}")
            except Exception as e:
                error(f"Could not create '{self._config_dir}': {e}")

        self._configs = [ e for e in listdir(self._config_dir) if path.isfile(path.normpath(self._config_dir + "/" + e)) and e.endswith(".conf") ]
        self._configs.sort()

    def present_config_selection(self):
        """
        Returns to path to an existing config or False if a new config should be created
        """
        # get configs
        if len(self._configs) == 0:
            info(f"No config valid file found in '{self._config_dir}'")
            return False

        print("0: create new configuration")
        for i, c in enumerate(self._configs):
            print(f"{i+1:2}: {c}")

        while True:
            choice = input("Please select a config: ")
            try:
                choice = int(choice)
            except ValueError:
                user_error(f"Invalid choice: '{choice}'. Choice must be a number between 0 and {len(self._configs)}")
                continue
            if not 0 <= choice <= len(self._configs):
                user_error(f"Invalid choice: '{choice}'. Choice must be a number between 0 and {len(self._configs)}")
                continue

            if choice == 0:
                return False
            return self._configs[choice-1]


    def _make_name(self, config_name: str):
        return path.normpath(self._config_dir + "/" + config_name.removesuffix(".conf") + ".conf")


    def write_config(self, config_name: str, keys: dict[str,str]):
        file = open(path.normpath(self._config_dir + "/" + config_name), 'w')
        file.write(f"# Config written by imgsort {version}.\n")
        for k, v in keys.items() :
            file.write(f"{k} = {v}\n")


    def read_config(self, config_name: str, root_directory="."):
        """
        @param root_directory Make all relative paths relative to this one
        """
        if type(config_name) != str:
            error(f"load config got wrong type: '{type(config_name)}'")
        config_file = self._make_name(config_name)
        if not path.isfile(config_file):
            error(f"File '{config_file}' does not exist")
        try:
            file = open(config_file, 'r')
        except Exception as e:
            error(f"Could not open file '{config_file}': {e}")

        keys: dict[str, str] = {}
        for i, line in enumerate(file.readlines()):
            line = line.replace("\n", "")
            match = re.fullmatch(r". = [^*?<>|]+", line)
            if match:
                key, value = line.split(" = ")
                keys[key]  = path.normpath(root_directory + "/" + value)
            elif not line[0] == "#":
                warning(f"In config file '{config_file}': Invalid line ({i+1}): '{line}'")
        self.validate_dirs(keys)
        return keys

    def create_config(self):
        keys: dict[str, str] = {}
        print(
f"""
===================================================================================================
Creating a new config
    You can now map keys to directories.
    The key must be one single letter, a single digit number or some other keyboard key like .-#+&/ ...
    The key can not be one of {' '.join(settings_map.keys())}.
    The directory must be a valid path to a directory, but is does not have to exist.
    You can use an absolute path (starting with '/', not '~') or a relative path (from here).
===================================================================================================
"""
        )

        while True:
            # ask for key
            key = input("Please enter a key or 'q' when you are done: ")
            if (len(key) != 1):
                user_error(f"Invalid key: '{key}' has a length other than 1")
                continue
            # if done
            elif key == 'q':
                if len(keys) == 0:
                    warning(f"No keys were mapped - exiting")
                    exit(0)
                save = input(f"\nDo you want to save the config to {self._config_dir}/<name>.conf?\nType a name to save the config or type 'q' to not save the config: ")
                if save != 'q':
                    self.write_config(save + ".conf", keys)
                break
            elif key in settings_map.keys():
                user_error(f"Invalid key: '{key}' is reserved and can not be mapped")
                continue

            # ask for directory
            directory = input("Please enter the directory/path: ")
            # match = re.match(r"/?([a-z-A-ZöÖäÄüÜ0-9/: _\-]+/)*[a-z-A-ZöÖäÄüÜ0-9/: _\-]+/?", directory)
            INVALID_PATH_CHARS = r":*?<>|"
            if any(c in INVALID_PATH_CHARS for c in directory):
                user_error(f"Invalid directory path: '{directory}' contains at least one if '{INVALID_PATH_CHARS}'")
                continue
            keys[key] = directory
            print(f"Added: {key}: '{directory}'\n")

        self.validate_dirs(keys)

        return keys


    def validate_dirs(self, keys):
        """
        Create the directories that dont exist.
        """
        missing = []
        for d in keys.values():
            if not path.isdir(d):
                missing.append(d)
        if len(missing) == 0: return
        print(f"The following directories do not exist:")
        for d in missing: print(f"\t{d}")
        decision = input(f"Create the ({len(missing)}) missing directories? y/*: ")
        if (decision == "y"):
            for d in missing:
                create_dir(d)
        else:
            error("Exiting - can not use non-existing directories.")


