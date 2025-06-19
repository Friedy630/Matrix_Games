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
    "light_green": (0, 64, 16),
}
# Tetris Tetromino-Farben laut offizieller Guideline

brightness = 64

pixels = np.full((16, 16, 3), colors["background"])


def set_pixel(x: int, y: int, color: tuple):
    if x >= 16 or x < 0:
        return
    if y >= 0 and y < 16:
        scaled_color = tuple((c * brightness) // 255 for c in color)
        display.set_xy((x % 16, y), scaled_color)
        pixels[x % 16, y] = color


def get_pixel(x: int, y: int):
    if x < 0 or x >= 16:
        return (255, 255, 255)
    if y >= 16:
        return (255, 255, 255)
    elif y >= 0:
        return tuple(pixels[x % 16, y])
    else:
        return colors["background"]


def fill(color: tuple, override=True):
    global pixels
    for x in range(16):
        for y in range(16):
            set_pixel(x, y, color)
    if override:
        show()


def set_shape(shape_matrix: np.ndarray, offset: Vec, color: tuple):
    for x in range(shape_matrix.shape[0]):
        for y in range(shape_matrix.shape[1]):
            if shape_matrix[x, y] == 0:
                continue
            set_pixel(offset.x + x, offset.y + y, color)


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
                and get_pixel(position.x + x, position.y + y) != colors["background"]
            ):
                return False
    return True


def rotate(shape, isleft: bool):
    rotated_matrix = get_rotated_shape_matrix(shape, isleft)
    return rotated_matrix


def show():
    display.show()


def clear(override=True):
    fill(colors["background"], override)


def clear_row(row: int, color=colors["background"]):
    for x in range(16):
        set_pixel(x, row, color)


def clear_column(column: int, color=colors["background"]):
    for y in range(16):
        set_pixel(column, y, color)


def draw_image(image, x_offset, y_offset):
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            color = image[x, y]
            if not np.array_equal(color, colors["background"]):
                set_pixel(x + x_offset, y + y_offset, tuple(color))


def fade(factor: float):
    global pixels
    for x in range(16):
        for y in range(16):
            r, g, b = pixels[x, y]
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            pixels[x, y] = (r, g, b)
            display.set_xy((x, y), (r, g, b))
