# imgsort - Image Sorter
This is a python program for Linux that lets you easily sort images from one directory into other directories.
It lets you go through a folder of images and simply move them using a single key press, which you define at program startup.
This is very useful when you want to sort your phone's camera folder or messenger media folders.
For example, you could quickly go through your WhatsApp media (after copying it to your pc) and sort the images into different directories like *Selfies*, *Landscapes*, *Friends* etc.

## Usage
1. Navigate to the folder containing the images and run "imgsort". 
```shell
cd ~/Pictures
imgsort
```
2. When you run it the first time, you will be prompted to create a new config. That means you need to assign keyboard keys to directories in your filesystem.
    For example, you could use:
    - `f` = `~/Pictures/Family`
    - `v` = `~/Pictures/Vacation_2019`
    - `o` = `~/Pictures/Other`

    Note that `s`, `u` and `q` are reserved for *skip*, *undo* and *quit*, but you can use `S`, `U` and `Q` instead.
3. Save the config if you might want to use it again. The config file will be stored in `$XDG_CONFIG_DIR` or `~/.config/imgsort`.
4. Enjoy the slideshow!

## Installation
Clone this repository and install it using python-pip.
This project depends on ueberzug to display the images in the terminal.
The original ueberzug is no longer maintained, but there is [a continuation](https://github.com/ueber-devel/ueberzug/) as well as a [new C++ alternative](https://github.com/jstkdng/ueberzugpp) available.

For the version supporting the original **ueberzug**:
```shell
git clone https://github.com/MatthiasQuintern/imgsort.git
cd imgsort
python3 -m pip install .
```
For the version supporting the new **ueberzug++**:
```shell
git clone --branch ueberzugpp https://github.com/MatthiasQuintern/imgsort.git
cd imgsort
python3 -m pip install .
```

## Changelog
### 1.2
- Works with ueberzugpp
- Use pyproject.toml for installation

### 1.2
- Support ueberzugpp
- Added option to open file with `xdg-open`
- Use pyproject.toml for installation

### 1.1
- Terminal does not break anymore when program exits
- Todo-Images are now sorted by filename

### 1.0
- Initial Release

## Importand Notice:
This software comes with no warranty!
