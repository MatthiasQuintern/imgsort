#!/bin/python3

import argparse
import curses as c
import os
from os import path, getcwd, listdir, makedirs, rename
import subprocess

if __name__ == "__main__":  # make relative imports work as described here: https://peps.python.org/pep-0366/#proposed-change
    if __package__ is None:
        __package__ = "imgsort"
        import sys
        filepath = path.realpath(path.abspath(__file__))
        sys.path.insert(0, path.dirname(path.dirname(filepath)))

from .ueberzug import UeberzugLayer

from .configs import ConfigManager
from .globals import version, settings_map
from .globals import warning, error, user_error, info, create_dir

# Size settings
FOOTER_LEFT = 0
FOOTER_HEIGHT = 2

SIDEBAR_WIDTH = 40

CURSOR_X = 0
CURSOR_Y = 2

KEYS_BEGIN = 5

class Sorter:
    def __init__(self, wdir, config):
        self.wd = wdir

        self.images = [] # old paths
        self.images_new = [] # new paths
        self.image_iter = 0
        self.image = ""

        self.keys = config

        self.settings = settings_map

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
        self._ueberzug = UeberzugLayer(pid_file="/tmp/ueberzu-imgsort.pid")
        self._img_x = SIDEBAR_WIDTH + 1
        self._img_y = 2
        self._img_width = self.win_x - SIDEBAR_WIDTH - 1
        self._img_height = self.win_y - FOOTER_HEIGHT - 2
        self._img_identifier = "imgsort_preview"




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
        self._ueberzug.display_image(self.image, x=self._img_x, y=self._img_y, max_width=self._img_width, max_height=self._img_height, identifier=self._img_identifier)
        self.window.addnstr(0, SIDEBAR_WIDTH + 1, self.image, self.win_x - SIDEBAR_WIDTH - 1)


    def sort(self):
        """
        Loop until all images are processed
        """
        while (self.image_iter < len(self.images)):
            self.image = self.images[self.image_iter]

            self.print_window()
            self.display_image()

            self.pressed_key = self.window.getkey() # wait until user presses something

            # check for quit, skip, undo or open
            if self.pressed_key in self.settings:
                if self.settings[self.pressed_key] == "quit":
                    self.quit(f"Key '{self.pressed_key}' pressed. Canceling image sorting")
                elif self.settings[self.pressed_key] == "skip":
                    self.image_iter += 1
                    self.message = "Skipped image"
                    continue
                elif settings_map[self.pressed_key] == "undo":
                    if self.image_iter > 0:
                        self.image_iter -= 1 # using last image
                        rename(self.images_new[self.image_iter], self.images[self.image_iter])
                        self.images_new[self.image_iter] = self.images[self.image_iter]
                        self.message = "Undone last action"
                        continue
                    else:
                        self.message = "Nothing to undo!"
                        continue
                elif settings_map[self.pressed_key] == "open":
                    try:
                        subprocess.run(['xdg-open', self.image], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                        self.message = "Opening with xdg-open"
                    except Exception as e:
                        print(f"open: Error: {e}")
                    continue

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
        self.win_y, self.win_x = self.window.getmaxyx()

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
            # show only last part
            v = v.split("/")[-1]
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
        print(message)
        print(f"Quitting imgsort {version}")
        exit(0)

    def __del__(self):
        self.window.clear()
        self.window.refresh()
        c.endwin()


def main():
    # set working directory
    print("""
===================================================================================================
Image Sorter
===================================================================================================
""")
    config_dir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "imgsort")
    # check if environment variables are set and use them if they are
    if 'IMGSOSRT_CONFIG_DIR' in os.environ: config_dir = os.environ['IMGSORT_CONFIG_DIR']

    parser = argparse.ArgumentParser("imgsort")
    parser.add_argument("-c", "--config", action="store", help="name of the config file in ($IMGSORT_CONFIG_DIR > $XDG_CONFIG_HOME/imgsort > ~/.config/imgsort)", default=None)
    parser.add_argument("-i", "--sort-dir", action="store", help="the directory where the folders from the config will be created")
    args = parser.parse_args()

    wd = getcwd();

    if args.sort_dir:
        args.sort_dir = path.abspath(args.sort_dir)
    else:
        args.sort_dir = getcwd()

    confman = ConfigManager(config_dir)

    # configuration
    if not args.config:
        args.config = confman.present_config_selection()
    # if create config was selected
    if args.config is False:
        config = confman.create_config()
    else:
        if type(args.config) != str:
            error(f"Could not determine condig file to load ('{args.config}' is of type '{type(args.config)}' not ")
        config = confman.read_config(args.config, args.sort_dir)

    sorter = Sorter(wd, config)
    sorter.get_images()
    sorter.sort()


if __name__ == "__main__":
    main()
