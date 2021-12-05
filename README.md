# imgsort - Image Sorter
This is a python program that lets you easily sort images from one directory into other directories.
For example, you could go through your phone's camera folder and sort the images into different folders, like *Family*, *Landscapes*, *Friends* etc.

## Usage
1. Navigate to the folder containing the images and run "imgsort". 
```shell
cd ~/Pictures
imgsort
```
2. When you run it the first time, you will be prompted to create a new config. That means you need to assign keyboard keys to directories in your filesystem.
    For example, you could use:
    - f = *~/Pictures/Family*
    - v = *~/Pictures/Vacation_2019*
    - o = *~/Pictures/Other*

    Note that 's', 'u' and 'q' are reserved for 'skip', 'undo' and 'quit', but you can use 'S', 'U' and 'Q' instead.
3. Save the config if you might want to use it again. The config file will be stored in *~/.config/imgsort*.
4. Enjoy the slideshow!

## Installation
Clone this repository and install it using python-pip.
pip should also install https://github.com/seebye/ueberzug, which lets you view images in a terminal.
```shell
cd ~/Downloads
git clone https://github.com/MatthiasQuintern/imgsort.git
cd imgsort
python3 -m pip install .
```
You can also install it system-wide using `sudo python3 -m pip install.`

## Changelog
### 1.1
- Terminal does not break anymore when program exits
- Todo-Images are now sorted by filename

### 1.0
Initial Release

## Importand Notice:
This software comes with no warranty!
