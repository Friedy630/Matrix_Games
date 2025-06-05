import numpy as np
import random as rng
from ulib import display, remote
import time
from lib import graphics_library as gl
from lib import input_library as il

# <SETTINGS>
side_to_side_pass = True

enable_win_screen = (
    True  # if the screen gets completely cleared, you win. TODO: not implemented yet
)

enable_exotic_shapes = False  # adds 20 more exiting shapes

exotic_shape_chance = 0.3  # chance to spawn an exotic shape instead of a normal one

enable_acceleration = False  # makes the falling speed accelerate over time

fall_step_interval_seconds = (
    0.700  # how much time it takes for the shape to fall one block
)

fall_step_interval_seconds = (
    0.700  # how much time it takes for the shape to fall one block
)

enable_shape_weights = True  # spawns each block with a given chance

diff1_step_interval_seconds = 1.0
diff2_step_interval_seconds = 0.75
diff3_step_interval_seconds = 0.5

# </STETTINGS>

currentShapeID = -1

current_shape_matrix = np.zeros((3, 3))
current_shape_position = gl.Vec(0, 0)
current_shape_color = (255, 255, 255)

fall_step_interval_seconds = diff1_step_interval_seconds

running = False

score = 0

exotic_weights_sum = 100

exotic_color = (100, 100, 100)  # color of any exotic shape

exotic_shapes = [
    (
        np.array(
            [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 1, 1],
                [0, 0, 1],
                [0, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 1],
                [0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 1],
                [0, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [1, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 1, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 1],
                [1, 1, 0],
                [0, 1, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 1, 1],
                [0, 0, 1],
                [0, 0, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 1, 1],
                [1, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [0, 0, 0],
                [1, 1, 0],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
    (
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
    ),
]

# Tetris Tetromino-Farben laut offizieller Guideline
shapes = [
    (
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]
        ).T,
        15,
        (0, 0, 255),
    ),  # J
    (np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]]).T, 10, (0, 255, 0)),  # S
    (
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]).T,
        20,
        (0, 255, 255),
    ),  # I
    (np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]]).T, 15, (128, 0, 128)),  # T
    (
        np.array(
            [
                [1, 1],
                [1, 1],
            ]
        ).T,
        15,
        (255, 255, 0),
    ),  # O
    (np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]]).T, 10, (255, 0, 0)),  # Z
    (np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]]).T, 15, (255, 165, 0)),  # L
]

weights_sum = 100

background_color = (0, 0, 0)
pixels = np.full((16, 16, 3), background_color)


def setpixel(x: int, y: int, color: tuple):
    if (x >= 16 or x < 0) and not side_to_side_pass:
        return
    if y >= 0 and y < 16:
        display.set_xy((x % 16, y), color)
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


def set_shape(shape_matrix: np.ndarray, offset, color: tuple):
    for x in range(shape_matrix.shape[0]):
        for y in range(shape_matrix.shape[1]):
            if shape_matrix[x, y] == 0:
                continue
            setpixel(offset.x + x, offset.y + y, color)


def get_rotated_shape_matrix(shape_matrix: np.ndarray, isleft: bool):
    return gl.get_rotated_shape_matrix(shape_matrix, isleft)


def check_fit(shape_matrix: np.ndarray, position: gl.Vec):
    return gl.check_fit(shape_matrix, position)


def remove_row(row: int):
    for y in range(row, 0, -1):
        for x in range(16):
            gl.setpixel(x, y, gl.getpixel(x, y - 1))


def check_for_full_row():
    global score
    block_counter = 0
    local_score = 0
    score_multiplier = 0
    for row in range(16):
        for col in range(16):
            if tuple(gl.pixels[col, row]) != gl.background_color:
                block_counter += 1
        if block_counter == 16:
            remove_row(row)
            local_score += 100
            score_multiplier += 1
        block_counter = 0
    score += local_score * score_multiplier


def paste_current_shape():
    gl.set_shape(current_shape_matrix, current_shape_position, current_shape_color)


def cut_current_shape():
    gl.set_shape(current_shape_matrix, current_shape_position, gl.background_color)


def move_horizontal(isleft: bool):
    global current_shape_position
    moved_position = current_shape_position
    if isleft:
        moved_position += gl.Vec(-1, 0)
    else:
        moved_position += gl.Vec(1, 0)
    cut_current_shape()
    if check_fit(current_shape_matrix, moved_position):
        current_shape_position = moved_position
    paste_current_shape()


def move_down():
    global current_shape_position
    moved_position = current_shape_position + gl.Vec(0, 1)
    cut_current_shape()
    if not check_fit(current_shape_matrix, moved_position):
        if current_shape_position.y < 0:
            print("game over")
            il.inputs["escape"] = True
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
    i = -1  # shape_index
    while w < randInt:
        i += 1
        w += weights_array[i][1]
    return i


def set_standard_shape():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = rng.randint(0, len(shapes) - 1)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = shapes[new_shape_id][0]
    current_shape_color = shapes[new_shape_id % len(shapes)][2]


def set_exotic_shape():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = rng.randint(0, len(exotic_shapes) - 1)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = exotic_shapes[new_shape_id][0]
    current_shape_color = exotic_color


def set_standard_shape_weighted():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = get_loottable_hit(shapes, weights_sum)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = shapes[new_shape_id][0]
    current_shape_color = shapes[new_shape_id][2]


def set_exotic_shape_weighted():
    global currentShapeID, current_shape_color, current_shape_matrix
    while True:
        new_shape_id = get_loottable_hit(exotic_shapes, exotic_weights_sum)
        if new_shape_id != currentShapeID:
            currentShapeID = new_shape_id
            break
    current_shape_matrix = exotic_shapes[new_shape_id][0]
    current_shape_color = exotic_color


def get_new_shape():
    global fall_step_interval_seconds, current_shape_matrix, current_shape_position, current_shape_color
    current_shape_position = gl.Vec(6, -2)
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


def start_tetris():
    print("entered tetris game")
    start_time = time.time()
    gl.fill(gl.background_color)
    get_new_shape()
    while running:
        if time.time() - start_time >= fall_step_interval_seconds:
            start_time = time.time()
            il.inputs["down"] = True
        if il.inputs["left"] != il.inputs["right"]:
            move_horizontal(il.inputs["left"])
        if il.inputs["up"] != il.inputs["space"]:
            rotate(il.inputs["up"])
        if il.inputs["down"] or il.inputs["enter"]:
            move_down()
        if il.inputs["escape"]:
            break
        il.reset_inputs()
        time.sleep(0.1)
        display.show()
    il.reset_inputs()


# Shapes for menu
close_x_shape = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
space_shape = np.array([[1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]])
s_shape = np.array([[1, 1], [1, 0], [1, 1], [0, 1], [1, 1]]).T
p_shape = np.array([[1, 1], [1, 1], [1, 1], [1, 0], [1, 0]]).T
e_shape = np.array([[1, 1], [1, 0], [1, 1], [1, 0], [1, 1]]).T
d_shape = np.array([[1, 0], [1, 1], [1, 1], [1, 1], [1, 0]]).T

progress_bar_border_shape = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
).T

progress_bar_inner_green_shape = np.array([[1, 1, 1], [1, 1, 1]]).T
progress_bar_inner_yellow_shape = np.array([[1, 1, 1, 1], [1, 1, 1, 1]]).T
progress_bar_inner_red_shape = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]).T


def start_main_menu():
    global running, fall_step_interval_seconds
    print("entered main menu")
    fall_step_interval_seconds = diff1_step_interval_seconds
    gl.fill((2, 2, 2))
    gl.set_shape(progress_bar_border_shape, gl.Vec(1, 1), (60, 60, 60))
    gl.set_shape(progress_bar_inner_green_shape, gl.Vec(2, 2), (0, 128, 0))
    gl.set_shape(s_shape, gl.Vec(1, 7), (60, 60, 60))
    gl.set_shape(p_shape, gl.Vec(4, 7), (60, 60, 60))
    gl.set_shape(e_shape, gl.Vec(7, 7), (60, 60, 60))
    gl.set_shape(e_shape, gl.Vec(10, 7), (60, 60, 60))
    gl.set_shape(d_shape, gl.Vec(13, 7), (60, 60, 60))
    display.show()
    while running:
        if il.inputs["escape"]:
            running = False
        if il.inputs["space"]:
            return True
        if fall_step_interval_seconds == diff1_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(
                    progress_bar_inner_yellow_shape, gl.Vec(5, 2), (128, 128, 0)
                )
                display.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        if fall_step_interval_seconds == diff2_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(progress_bar_inner_red_shape, gl.Vec(9, 2), (128, 0, 0))
                display.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff3_step_interval_seconds
            if il.inputs["left"]:
                gl.set_shape(progress_bar_inner_yellow_shape, gl.Vec(5, 2), (2, 2, 2))
                display.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff1_step_interval_seconds
        if fall_step_interval_seconds == diff3_step_interval_seconds:
            if il.inputs["left"]:
                gl.set_shape(progress_bar_inner_red_shape, gl.Vec(9, 2), (2, 2, 2))
                display.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        il.reset_inputs()
        time.sleep(0.1)
    return False


def main():
    global running
    remote.listen()
    remote.bind_all(il.register_input)
    running = True
    while start_main_menu():
        start_tetris()
    running = False
    remote.unbind_all(il.register_input)
    gl.fill(gl.background_color)


# program

remote.start_pygame_thread()

print("startup")
main()
print("exited")

remote.close_pygame_thread()
