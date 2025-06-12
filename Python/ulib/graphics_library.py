import numpy as np
from ulib import display
from dataclasses import dataclass


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    @classmethod
    def zero(cls):
        return cls(0, 0)


# Tetromino types as string keys for dict (emulating enum functionality)
colors = {
    "cyan": (0, 255, 255),
    "blue": (0, 0, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "background": (0, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "grey": (128, 128, 128),
    "light_grey": (192, 192, 192),
    "dark_grey": (64, 64, 64),
    "light_green": (64, 192, 64),
}
# Tetris Tetromino-Farben laut offizieller Guideline

brightness = 96

pixels = np.full((16, 16, 3), colors["background"])


def setpixel(x: int, y: int, color: tuple):
    if x >= 16 or x < 0:
        return
    if y >= 0 and y < 16:
        scaled_color = tuple((c * brightness) // 255 for c in color)
        display.set_xy((x % 16, y), scaled_color)
        pixels[x % 16, y] = color


def getpixel(x: int, y: int):
    if x < 0 or x >= 16:
        return (255, 255, 255)
    if y >= 16:
        return (255, 255, 255)
    elif y >= 0:
        return tuple(pixels[x % 16, y])
    else:
        return colors["background"]


def fill(color: tuple):
    display.fill(color)
    for y in range(16):
        for x in range(16):
            pixels[x, y] = color


def set_shape(shape_matrix: np.ndarray, offset: Vec, color: tuple):
    for x in range(shape_matrix.shape[0]):
        for y in range(shape_matrix.shape[1]):
            if shape_matrix[x, y] == 0:
                continue
            setpixel(offset.x + x, offset.y + y, color)


def get_rotated_shape_matrix(shape_matrix: np.ndarray, isleft: bool):
    if isleft:
        return np.rot90(shape_matrix, 1)
    else:
        return np.rot90(shape_matrix, -1)


def check_fit(shape_matrix: np.ndarray, position: Vec):
    for x in range(shape_matrix.shape[0]):
        for y in range(shape_matrix.shape[1]):
            if (
                shape_matrix[x, y] == 1
                and getpixel(position.x + x, position.y + y) != colors["background"]
            ):
                return False
    return True


def rotate(shape, isleft: bool):
    global current_shape_matrix
    rotated_matrix = get_rotated_shape_matrix(shape, isleft)
    return rotated_matrix


def show():
    display.show()
