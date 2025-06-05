import numpy as np
import random as rng
from ulib import display, remote
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

# <SETTINGS>

side_to_side_pass = False           #you can faze through the left/right borders

enable_win_screen = True            #if the screen gets completely cleared, you win. TODO: not implemented yet

enable_exotic_shapes = True         #adds 20 more exiting shapes

exotic_shape_chance = 0.3           #chance to spawn an exotic shape instead of a normal one

enable_acceleration = False         #makes the falling speed accelerate over time

fall_step_interval_seconds = 0.700  #how much time it takes for the shape to fall one block

enable_shape_weights = True        #spawns each block with a given chance

# </STETTINGS>

currentShapeID = -1

current_shape_matrix = np.zeros((3, 3))
current_shape_position = Vec(0, 0)
current_shape_color = (255, 255, 255)
running = False

score = 0

exotic_shapes_weights = [
    5, #01
    5, #02
    5, #03
    5, #04
    5, #05
    5, #06
    5, #07
    5, #08
    5, #09
    5, #10
    5, #11
    5, #12
    5, #13
    5, #14
    5, #15
    5, #16
    5, #17
    5, #18
    5, #19
    5, #20
]

exotic_weights_sum = 100

exotic_color = (100, 100, 100)  #color aof any exotic shape

exotic_shapes = [
    np.array(
        [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ).T,
    np.array(
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ]
    ).T,
    np.array(
        [
            [0, 1, 1],
            [0, 0, 1],
            [0, 1, 1],
        ]
    ).T,
    np.array(
        [
            [1, 1],
            [0, 0],
        ]
    ).T,
    np.array(
        [
            [1, 1],
            [0, 1],
        ]
    ).T,
    np.array(
        [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 0],
        ]
    ).T,
    np.array(
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 1],
        ]
    ).T,
    np.array(
        [
            [0, 0, 1],
            [1, 1, 1],
            [1, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 1, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 1],
            [1, 1, 0],
            [0, 1, 0],
        ]
    ).T,
    np.array(
        [
            [1, 1, 1],
            [0, 0, 1],
            [0, 0, 1],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 1, 1],
            [0, 0, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
        ]
    ).T,
    np.array(
        [
            [0, 0, 0],
            [1, 1, 0],
            [1, 1, 1],
        ]
    ).T,
    np.array(
        [
            [1, 0, 0],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ).T
]

shapes_weights = [
    15, #1
    10, #2
    20, #3
    15, #4
    15, #5
    10, #6
    15, #7
]

weights_sum = 100


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
    (0, 0, 255),
    (0, 255, 0),
    (0, 255, 255),
    (128, 0, 128),
    (255, 255, 0),
    (255, 0, 0),
    (255, 165, 0),
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


def get_loottable_hit(weights_array, weights_sum):
    randInt = rng.randint(0, weights_sum - 1)
    w = 0
    i = -1 #shape_index
    while w < randInt:
         i += 1
         w += weights_array[i]
    return i

def set_standard_shape():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = rng.randint(0, len(shapes) - 1)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = shapes[new_shape_id]
    current_shape_color = colors[new_shape_id % len(colors)]

def set_exotic_shape():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = rng.randint(0, len(exotic_shapes) - 1)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = exotic_shapes[new_shape_id]
    current_shape_color = exotic_color
    

def set_standard_shape_weighted():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = get_loottable_hit(shapes_weights, weights_sum)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = shapes[new_shape_id]
    current_shape_color = colors[new_shape_id]

def set_exotic_shape_weighted():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = get_loottable_hit(exotic_shapes_weights, exotic_weights_sum)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = exotic_shapes[new_shape_id]
    current_shape_color = exotic_color


def get_new_shape():
    global fall_step_interval_seconds, current_shape_matrix, current_shape_position, current_shape_color
    current_shape_position = Vec(6, -2)
    spawn_exotic = False
    if enable_exotic_shapes:
        spawn_exotic = rng.randint(0, 99) / 100.0 <= exotic_shape_chance
    else:
        spawn_exotic = False
    if spawn_exotic:
        if enable_shape_weights:
            set_exotic_shape_weighted()
        else:
            set_exotic_shape()
    else:
        if enable_shape_weights:
            set_standard_shape_weighted()
        else:
            set_standard_shape()
    paste_current_shape()
    if enable_acceleration:
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


def start_main_menu():
    global running
    print("entered main menu")
    fill((20, 20, 20))
    set_shape(close_x_shape, Vec(1, 1), (200, 100, 120))
    set_shape(get_rotated_shape_matrix(space_shape, True), Vec(4, 10), (100, 180, 120))
    # Create a (12,6) array with a (10,4) block of zeros offset inside
    arr = np.zeros((14, 6))
    arr[1:13, 1:5] = 1  # Offset by (1,1)
    box = np.ones((14, 6)) - arr
    set_shape(box, Vec(1, 8), (120, 200, 150))
    display.show()
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
