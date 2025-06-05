import numpy as np
import random as rng
from ulib import display
from ulib import remote
from dataclasses import dataclass
import time


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)


colors = [
    (0, 0, 255),  # Blau
    (0, 255, 0),  # Grün
    (0, 255, 255),  # Cyan
    (128, 0, 128),  # Lila
    (255, 255, 0),  # Gelb
    (255, 0, 0),  # Rot
    (255, 165, 0),  # Orange
]
# Tetris Tetromino-Farben laut offizieller Guideline

background_color = (0, 0, 0)
pixels = np.full((16, 16, 3), background_color)


def setpixel(x: int, y: int, color: tuple):
    if x >= 16 or x < 0:
        return
    if y >= 0 and y < 16:
        display.set_xy(x % 16, y, color)
        pixels[x % 16, y] = color


def getpixel(x: int, y: int):
    if x < 0 or x >= 16:
        return (255, 255, 255)
    if y >= 16:
        return (255, 255, 255)
    elif y >= 0:
        return tuple(pixels[x % 16, y])
    else:
        return background_color


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
                and getpixel(position.x + x, position.y + y) != background_color
            ):
                return False
    return True


def rotate(shape, isleft: bool):
    global current_shape_matrix
    rotated_matrix = get_rotated_shape_matrix(shape, isleft)
    return rotated_matrix
