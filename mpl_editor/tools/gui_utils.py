import os
from pathlib import Path

import matplotlib
from PyQt5 import QtGui

ROOT_DIR = Path(__file__).parent.parent
IMAGE_DIR = ROOT_DIR / 'images'


# Images #####################################################################


def get_image_dir():
    return IMAGE_DIR


def get_image_path(filename):
    return IMAGE_DIR / filename


def get_icon(name):
    name = Path(name)
    if name.suffix == "":
        name = name.with_suffix(".png")
    img_file = get_image_path(name)
    if not img_file.is_file():
        img_file = Path(matplotlib.get_data_path()) / 'images' / name
        if not img_file.is_file():
            raise IOError(f"Image '{img_file}' not found.")
    return QtGui.QIcon(str(img_file))

