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

side_to_side_pass = True;

current_shape_matrix = np.zeros((3, 3))
current_shape_position = Vec(0, 0)
current_shape_color = (255, 255, 255)

diff1_step_interval_seconds = 1.0
diff2_step_interval_seconds = 0.75
diff3_step_interval_seconds = 0.5

fall_step_interval_seconds = diff1_step_interval_seconds

running = False

score = 0

shapes = [
    np.array(
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]
    ).T, # J
    np.array(
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ]
    ).T, # S
    np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ]
    ).T, # I
    np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
    ).T, # T
    np.array(
        [
            [1, 1],
            [1, 1],
        ]
    ).T, # O
    np.array(
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ]
    ).T, # Z
    np.array(
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ]
    ).T, # L
]

colors = [
    (0, 0, 255), # Blau
    (0, 255, 0), # Grün
    (0, 255, 255), # Cyan
    (128, 0, 128), # Lila
    (255, 255, 0), # Gelb
    (255, 0, 0), # Rot
    (255, 165, 0), # Orange
]
# Tetris Tetromino-Farben laut offizieller Guideline

background_color = (0, 0, 0)
pixels = np.full((16, 16, 3), background_color)


def setpixel(x: int, y: int, color: tuple):
    if (x >= 16 or x < 0) and not side_to_side_pass:
        return
    if y >= 0 and y < 16:
        display.set_xy(x % 16, y, color)
        pixels[x % 16, y] = color


def getpixel(x: int, y: int):
    if (x < 0 or x >= 16) and not side_to_side_pass:
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
    new_shape_id = rng.randint(0, 6)
    current_shape_matrix = shapes[new_shape_id]
    current_shape_color = colors[new_shape_id]
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


close_x_shape = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
space_shape = np.array([[1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]])
s_shape = np.array(
    [
        [1, 1],
        [1, 0],
        [1, 1],
        [0, 1],
        [1, 1]
    ]
).T

p_shape = np.array(
    [
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 0],
        [1, 0]
    ]
).T

e_shape = np.array(
    [
        [1, 1],
        [1, 0],
        [1, 1],
        [1, 0],
        [1, 1]
    ]
).T

d_shape = np.array(
    [
        [1, 0],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 0]
    ]
).T

progress_bar_border_shape = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
).T

progress_bar_inner_green_shape = np.array(
    [
        [1, 1, 1],
        [1, 1, 1]
    ]
).T

progress_bar_inner_yellow_shape = np.array(
    [
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
).T

progress_bar_inner_red_shape = np.array(
    [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
).T

def start_main_menu():
    global running, fall_step_interval_seconds
    print("entered main menu")
    fill((20, 20, 20))
    set_shape(progress_bar_border_shape, Vec(1, 1), (120, 120, 120))
    set_shape(progress_bar_inner_green_shape, Vec(2, 2), (0, 255, 0))
    set_shape(s_shape, Vec(1, 7), (120, 120, 120))
    set_shape(p_shape, Vec(4, 7), (120, 120, 120))
    set_shape(e_shape, Vec(7, 7), (120, 120, 120))
    set_shape(e_shape, Vec(10, 7), (120, 120, 120))
    set_shape(d_shape, Vec(13, 7), (120, 120, 120))
    # Create a (12,6) array with a (10,4) block of zeros offset inside
    arr = np.zeros((14, 6))
    arr[1:13, 1:5] = 1  # Offset by (1,1)

    display.show()
    while running:
        if inputs["escape"]:
            running = False
        if inputs["space"]:
            return True
        if fall_step_interval_seconds == diff1_step_interval_seconds:
            if inputs["right"]:
                set_shape(progress_bar_inner_yellow_shape, Vec(5, 2), (255, 255, 0))
                display.show()
                reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        if fall_step_interval_seconds == diff2_step_interval_seconds:
            if inputs["right"]:
                set_shape(progress_bar_inner_red_shape, Vec(9, 2), (255, 0, 0))
                display.show()
                reset_inputs()
                fall_step_interval_seconds = diff3_step_interval_seconds
            if inputs["left"]:
                set_shape(progress_bar_inner_yellow_shape, Vec(5, 2), (20, 20, 20))
                display.show()
                reset_inputs()
                fall_step_interval_seconds = diff1_step_interval_seconds
        if fall_step_interval_seconds == diff3_step_interval_seconds:
            if inputs["left"]:
                set_shape(progress_bar_inner_red_shape, Vec(9, 2), (20, 20, 20))
                display.show()
                reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
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
