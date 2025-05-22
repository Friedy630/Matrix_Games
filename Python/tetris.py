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


inputs = {
    "left": False,
    "right": False,
    "down": False,
    "up": False,
    "space": False,
    "enter": False,
    "escape": False,
}

current_shape_matrix = np.zeros((3, 3))
current_shape_position = Vec(0, 0)
current_shape_color = (255, 255, 255)
fall_step_interval_seconds = 0.700
running = False

score = 0

shapes = [
    np.array(
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]
    ).T,
    np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]]).T,
    np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]).T,
    np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]]).T,
    np.array(
        [
            [1, 1],
            [1, 1],
        ]
    ).T,
    np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]]).T,
    np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]]).T,
]

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (100, 100, 0),
    (0, 100, 100),
    (100, 0, 100),
]

background_color = (0, 0, 0)
pixels = np.full((16, 16, 3), background_color)


def setpixel(x: int, y: int, color: tuple):
    if x >= 0 and y >= 0 and x < 16 and y < 16:
        display.set_xy(x, y, color)
        pixels[x, y] = color


def getpixel(x: int, y: int):
    if x >= 0 and x < 16 and y < 16:
        if y >= 0:
            return tuple(pixels[x, y])
        else:
            return background_color
    else:
        return (255, 255, 255)


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


def remove_row(row: int):
    for y in range(row, 0, -1):
        for x in range(16):
            setpixel(x, y, getpixel(x, y - 1))


def check_for_full_row():
    global score
    block_counter = 0
    local_score = 0
    score_multiplier = 0
    for row in range(16):
        for col in range(16):
            if tuple(pixels[col, row]) != background_color:
                block_counter += 1
        if block_counter == 16:
            remove_row(row)
            local_score += 100
            score_multiplier += 1
        block_counter = 0
    score += local_score * score_multiplier


def paste_current_shape():
    set_shape(current_shape_matrix, current_shape_position, current_shape_color)


def cut_current_shape():
    set_shape(current_shape_matrix, current_shape_position, background_color)


def move_horizontal(isleft: bool):
    global current_shape_position
    moved_position = current_shape_position
    if isleft:
        moved_position += Vec(-1, 0)
    else:
        moved_position += Vec(1, 0)
    cut_current_shape()
    if check_fit(current_shape_matrix, moved_position):
        current_shape_position = moved_position
    paste_current_shape()


def move_down():
    global current_shape_position
    moved_position = current_shape_position + Vec(0, 1)
    cut_current_shape()
    if not check_fit(current_shape_matrix, moved_position):
        if current_shape_position.y < 0:
            print("game over")
            inputs["escape"] = True
        else:
            paste_current_shape()
            check_for_full_row()
            get_new_shape()
        return
    current_shape_position = moved_position
    paste_current_shape()


def rotate(isleft: bool):
    global current_shape_matrix
    rotated_matrix = get_rotated_shape_matrix(current_shape_matrix, isleft)
    cut_current_shape()
    if check_fit(rotated_matrix, current_shape_position):
        current_shape_matrix = rotated_matrix
    paste_current_shape()


def get_new_shape():
    global fall_step_interval_seconds, current_shape_matrix, current_shape_position, current_shape_color
    current_shape_position = Vec(6, -2)
    current_shape_matrix = rng.choice(shapes)
    current_shape_color = rng.choice(colors)
    paste_current_shape()
    fall_step_interval_seconds *= 0.98


def register_input(key: str):
    global running
    if key in inputs:
        inputs[key] = True
    if key == "exit":
        running = False  # exit-flag, wird von pygame gesetzt, könnte man aus dem code werfen später


def reset_inputs():
    for key in inputs:
        inputs[key] = False


def start_tetris():
    print("entered tetris game")
    start_time = time.time()
    fill(background_color)
    get_new_shape()
    while running:
        if time.time() - start_time >= fall_step_interval_seconds:
            start_time = time.time()
            inputs["down"] = True
        if inputs["left"] != inputs["right"]:
            move_horizontal(inputs["left"])
        if inputs["up"] != inputs["space"]:
            rotate(inputs["up"])
        if inputs["down"] or inputs["enter"]:
            move_down()
        if inputs["escape"]:
            break
        reset_inputs()
        time.sleep(0.1)
        display.show()
    reset_inputs()


def start_main_menu():
    global running
    print("entered main menu")
    fill((20, 120, 20))
    while running:
        if inputs["escape"]:
            running = False
        if inputs["space"]:
            return True
        reset_inputs()
        time.sleep(0.1)  # muss hier sein, damit das programm ich schließen lässt
        # start menu code here...
    return False


def main():
    global running
    remote.listen()
    remote.bind_all(register_input)
    running = True
    while start_main_menu():
        start_tetris()
    running = False
    remote.unbind_all(register_input)
    fill(background_color)


# program

remote.start_pygame_thread()

print("startup")
main()
print("exited")

remote.close_pygame_thread()
