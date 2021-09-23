# imgsort - Glowzwiebel Image Sorter
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
    - v = *~/Pictures/Vacation 2019*
    - o = *~/Pictures/Other*
3. Save the config if you might want to use it again. The config file will be stored in *~/.config/imgsort*.
4. Enjoy the slideshow!

## Installation
##### 1. With pip
Clone this repository using `git clone https://github.com/MatthiasQuintern/imgsort.git`.
Go into the the downloaded folder using `cd imgsort`.
Install with pip using `python3 -m pip install .` or `pip3 install .`.
pip should also install https://github.com/seebye/ueberzug, which lets you view images in a terminal.
