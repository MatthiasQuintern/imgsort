#!/bin/python3

import curses as c
import ueberzug.lib.v0 as uz

<<<<<<< HEAD

from os import path, getcwd, listdir, mkdir, makedirs, rename
import subprocess

if __name__ == "__main__":  # make relative imports work as described here: https://peps.python.org/pep-0366/#proposed-change
    if __package__ is None:
        __package__ = "imgsort"
        import sys
        filepath = path.realpath(path.abspath(__file__))
        sys.path.insert(0, path.dirname(path.dirname(filepath)))

from .configs import read_config, write_config, select_config, create_config

settings = {
            "q": "quit",
            "s": "skip",
            "u": "undo",
            "o": "open"
        }

# Size settings
FOOTER_LEFT = 0
FOOTER_HEIGHT = 2

SIDEBAR_WIDTH = 40

CURSOR_X = 0
CURSOR_Y = 2

KEYS_BEGIN = 5

version = "1.2-legacy"

class Sorter:
    def __init__(self, wdir, canvas, config):
        self.wd = wdir

        self.images = [] # old paths
        self.images_new = [] # new paths
        self.image_iter = 0
        self.image = ""

        self.keys = config

        self.settings = settings

        self.validate_dirs()

        # info about last action
        self.last_dir = ""

        # curses
        self.window = c.initscr()
        # c.start_color()
        # c.use_default_colors()
        self.win_y, self.win_x = self.window.getmaxyx()

        self.message = "" # displayed in footer
        self.pressed_key = ""

        c.echo()

        # ueberzug
        self.canvas = canvas

        self.placement = self.canvas.create_placement("p1", x=0, y=0, path="")
        self.placement.visibility = uz.Visibility.VISIBLE
        self.placement.scaler = uz.ScalerOption.FIT_CONTAIN.value
        self.placement.x = SIDEBAR_WIDTH + 1
        self.placement.y = 2
        self.placement.width = self.win_x - SIDEBAR_WIDTH - 1
        self.placement.height = self.win_y - FOOTER_HEIGHT - 2

    def validate_dirs(self):
        """
        Create the directories that dont exist.
        """
        for d in self.keys.values():
            if not path.isdir(d):
                print(f"Directory '{d}' does not exist.")
                decision = input(f"Create directory '{path.abspath(d)}'? y/n: ")
                if (decision == "y"):
                    makedirs(d)
                else:
                    print("Exiting - can not use non-existing directory.")
                    exit(1)


    def get_images(self):
        """
        Put all image-paths from wd in images dictionary.
        """
        self.images.clear()
        self.images_new.clear()

        for name in listdir(self.wd):
            name = path.normpath(self.wd + "/" + name)
            if (path.isfile(name)):
                self.images.append(name)

        self.images.sort()
        self.images_new = self.images.copy()
        # print(self.images)
            
    def display_image(self):
        with self.canvas.lazy_drawing: # issue ueberzug command AFTER with-statement
            self.placement.path = self.image
            self.window.addnstr(0, SIDEBAR_WIDTH + 1, self.placement.path, self.win_x - SIDEBAR_WIDTH - 1)

    def sort(self):
        """
        Loop until all images are processed
        """
        while (self.image_iter < len(self.images)):
            self.image = self.images[self.image_iter]

            self.print_window()
            self.display_image()

            self.pressed_key = self.window.getkey() # wait until user presses something

            # check for quit, skip or undo
            if self.pressed_key in self.settings:
                if self.settings[self.pressed_key] == "quit":
                    self.quit(f"Key '{self.pressed_key}' pressed. Canceling image sorting")
                elif self.settings[self.pressed_key] == "skip":
                    self.image_iter += 1
                    self.message = "Skipped image"
                    continue
                elif settings[self.pressed_key] == "undo":
                    if self.image_iter > 0:
                        self.image_iter -= 1 # using last image
                        rename(self.images_new[self.image_iter], self.images[self.image_iter])
                        self.images_new[self.image_iter] = self.images[self.image_iter]
                        self.message = "Undone last action"
                        continue
                    else:
                        self.message = "Nothing to undo!"
                        continue
                elif settings[self.pressed_key] == "open":
                    try:
                        subprocess.run(['xdg-open', self.image])
                        self.message = "Opening with xdg-open"
                    except Exception as e:
                        print(f"open: Error: {e}")

            # move to folder
            elif self.pressed_key in self.keys:
                new_filepath =  self.move_file(self.image, self.keys[self.pressed_key])
                if new_filepath: # is string when successful
                    self.images_new[self.image_iter] = new_filepath
                    self.message = f"Moved image to {self.keys[self.pressed_key]}"
                else:
                    self.message = f"ERROR: Failed to move '{self.image}' to '{self.keys[self.pressed_key]}'."
                self.image_iter += 1

        self.quit("All done!")

    def print_window(self):
        """
        Draw lines and text
        """
        self.window.erase()

        # lines
        self.window.hline(self.win_y - FOOTER_HEIGHT, FOOTER_LEFT, '=', self.win_x)
        self.window.vline(0, SIDEBAR_WIDTH, '|', self.win_y - FOOTER_HEIGHT + 1)

        # version
        version_str = f"imgsort {version}"
        x = self.win_x - len(version_str) - 1
        self.window.addstr(self.win_y - 1, x, version_str)

        # wd
        wdstring = f"Sorting {self.wd} - {len(self.images)} files - {len(self.images) - self.image_iter} remaining."
        self.window.addnstr(self.win_y - 1, FOOTER_LEFT, wdstring, self.win_x)

        # message
        self.window.addstr(self.win_y - FOOTER_HEIGHT, SIDEBAR_WIDTH + 2, self.message)
        self.message = ""

        # progress
        progstring = f"File {self.image_iter + 1}/{len(self.images)}"
        x = self.win_x - len(progstring) - 1
        self.window.addstr(self.win_y - FOOTER_HEIGHT, x, progstring)

        # print all key : action pairs
        i = 0
        self.window.hline(KEYS_BEGIN + i, 0, '-', SIDEBAR_WIDTH)
        i += 1
        self.window.addnstr(KEYS_BEGIN + i, 0, "Key: Action", SIDEBAR_WIDTH)
        i += 1
        self.window.hline(KEYS_BEGIN + i, 0, '-', SIDEBAR_WIDTH)
        i += 1
        for k, v in self.settings.items():
            if i >= self.win_y - KEYS_BEGIN - FOOTER_HEIGHT: # dont write into footer
                break
            if k == self.pressed_key:
                self.window.addnstr(KEYS_BEGIN + i, 0, f"  {k}: {v}", SIDEBAR_WIDTH, c.A_STANDOUT)
            else:
                self.window.addnstr(KEYS_BEGIN + i, 0, f"  {k}: {v}", SIDEBAR_WIDTH)
            i += 1
        self.window.hline(KEYS_BEGIN + i, 0, '-', SIDEBAR_WIDTH)
        i += 1

        # print all key : directory pairs
        self.window.addnstr(KEYS_BEGIN + i, 0, "Key: Directory", SIDEBAR_WIDTH)
        i += 1
        self.window.hline(KEYS_BEGIN + i, 0, '-', SIDEBAR_WIDTH)
        i += 1
        for k, v in self.keys.items():
            if i >= self.win_y - KEYS_BEGIN - FOOTER_HEIGHT: # dont write into footer
                break
            if k == self.pressed_key:
                self.window.addnstr(KEYS_BEGIN + i, 0, f"  {k}: {v}", SIDEBAR_WIDTH, c.A_STANDOUT)
            else:
                self.window.addnstr(KEYS_BEGIN + i, 0, f"  {k}: {v}", SIDEBAR_WIDTH)
            i += 1

        self.window.move(CURSOR_Y, CURSOR_X)

    def move_file(self, file, dest):
        # if not path.isdir(dest):
        #     makedirs(dest)
        if not path.isfile(file): return False
        if not path.isdir(dest): return False

        new_path = path.normpath(dest + '/' + path.split(file)[1])

        rename(file, new_path)
        return new_path

    def quit(self, message = ""):
        self.window.clear()
        self.window.refresh()
        c.endwin()
        print(message)
        print(f"Quitting imgsort {version}")
        exit(0)
    



def main():
    # set working directory
    print(f"""===================================================================================================
imgsort {version} - Image Sorter
===================================================================================================""")
    # set directories
    config_dir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "regina")
    # check if environment variables are set and use them if they are
    if 'IMGSOSRT_CONFIG_DIR' in os.environ: config_dir = os.environ['IMGSORT_CONFIG_DIR']

    parser = argparse.ArgumentParser(prog="imgsort")
    parser.add_argument("--config", "-c",   action="store",         help="name or path of config file", metavar="config file")
    parser.add_argument("--dir", "-d",      action="store",         help="working directory", metavar="working directory")
    args = parser.parse_args()

    # working directory
    if args.dir:
        if not path.isdir(args.dir):
            parser.error(f"invalid working directory: {args.wdir}")
        wd = path.abspath(args.dir)
        os.chdir(wd)
    else:
        wd = getcwd()

    # configuration
    if args.config:
        config_path = args.config_file
        # search locally
        if not path.isfile(config_path):
            config_path = path.join(config_dir, args.config)
            if not path.isfile(config_path):
                parser.error(f"invalid configuration path/name:'{config_path}'/'{args.config}'")
    else:
        config_path = select_config()
    print(config_path)
    if config_path is not None:
        config = read_config(config_path)
    else:
        config = create_config()

    if not config:
        print("Error reading the config:")
        print("  Config Name:", config_path)
        print("  Config:", config)
        exit(1)

    with uz.Canvas() as canvas:
        sorter = Sorter(wd, canvas, config)
        sorter.get_images()
        sorter.sort()


if __name__ == "__main__":
    main()
