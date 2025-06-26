import numpy as np
import random as rng
from ulib import display, remote
import time
from ulib import graphics_library as gl
from ulib import input_library as il

is_game_over = False

def restart():
    for obst in obstacle_instances:
        gl.set_shape(obstacles[obst[1]], obst[0], gl.colors["background"])
    obstacle_instances.clear()

max_jmp_height = 8
jump_height = 0
base_height = 4

player_pos = gl.Vec(2, 5)

obs_spawn_interval_min = 0.8     # in seconds
obs_spawn_interval_max = 1.5     # in seconds

ground_color = gl.colors["green"]
player_color = gl.colors["red"]
obstacle_color = gl.colors["white"]

# clock 1: player redraw clock
last_player_step_time = 0.0
player_step_interval = 0.01

def player_clock_step(current_time):
    global last_player_step_time
    if current_time - last_player_step_time >= player_step_interval:
        last_player_step_time = current_time
        player_step(current_time)

# clock 2: jump clock, so a jump cannot start when one is already in progress
last_jump_time = 0.0
jump_duration = 0.7

# gets set to true, if jump is pressed right before the jump ends; "forgiving controls"
jump_directly = False

def on_jump(current_time):
    global last_jump_time, jump_directly
    delta_time = current_time - last_jump_time
    if delta_time >= jump_duration:
        last_jump_time = current_time
        jump_directly = False
    elif jump_duration - delta_time <= 0.1:
        jump_directly = True

# clock 3: world redraw clock
last_world_step_time = 0.0
world_step_interval = 0.1

def world_clock_step(current_time):
    global last_world_step_time
    if current_time - last_world_step_time >= world_step_interval:
        last_world_step_time = current_time
        world_step()

# clock 4: obstacle spawn clock
last_spawn_time = 0.0
spawn_interval = 1

def spawn_clock_step(current_time):
    global last_spawn_time
    if current_time - last_spawn_time >= spawn_interval:
        last_spawn_time = current_time
        spawn_step()

def player_step(current_time):
    global jump_height, is_game_over
    if not check_fit(player_shape, player_pos):
        is_game_over = True
    gl.set_shape(player_shape, player_pos, gl.colors["background"])
    jump_height = max(0, max_jmp_height * (-(4 / (jump_duration**2)) * (((current_time - last_jump_time) - (jump_duration / 2))**2) + 1))
    player_pos.y = 16 - round(jump_height) - base_height - 2
    if not check_fit(player_shape, player_pos):
        is_game_over = True
    gl.set_shape(player_shape, player_pos, player_color)

def check_fit(shape_matrix: np.ndarray, position: gl.Vec):
    for x in range(shape_matrix.shape[0]):
        for y in range(shape_matrix.shape[1]):
            color = gl.get_pixel(position.x + x, position.y + y)
            if (
                shape_matrix[x, y] == 1
                and (color != gl.colors["background"] and color != player_color)
            ):
                return False
    return True

def world_step():
    for obst in obstacle_instances:
        gl.set_shape(obstacles[obst[1]], obst[0], gl.colors["background"])
    for obst in obstacle_instances:
        obst[0].x -= 1
    for obst in obstacle_instances:
        gl.set_shape(obstacles[obst[1]], obst[0], obstacle_color)

def spawn_step():
    global spawn_interval
    obstacle_instances.append((gl.Vec(16, 16 - base_height - 3), rng.randint(0, len(obstacles) - 1)))
    spawn_interval = obs_spawn_interval_min + rng.random() * (obs_spawn_interval_max - obs_spawn_interval_min)

player_shape = np.array(
    [
        [1, 1],
        [1, 1],
    ])

obstacles = [
    np.array([
        [1, 1],
        [1, 1],
        [1, 1]
    ]).T,
    np.array([
        [0, 0],
        [1, 1],
        [1, 1]
    ]).T,
    np.array([
        [0, 1],
        [1, 1],
        [1, 1]
    ]).T,
    np.array([
        [0, 1],
        [1, 0],
        [0, 1]
    ]).T,
]

obstacle_instances : list[tuple[gl.Vec, int]] = []

def jmp_formula(x):
    a = jump_duration
    return  


def start_dino():
    global running, is_game_over
    running = True
    restart()
    il.initialise()
    for y in range(base_height + 1):
        for x in range(16):
            gl.set_pixel(x, 16 - y, ground_color)
    while running:
        if il.inputs["exit"]:
            running = False
            return False
        if il.inputs["escape"]:
            running = False
        if is_game_over:
            if il.inputs["space"]:
                restart()
                is_game_over = False
        else:
            current_time = time.time()
            if il.inputs["up"] or jump_directly:
                on_jump(current_time)
            world_clock_step(current_time)
            spawn_clock_step(current_time)
            player_clock_step(current_time)
        il.reset_inputs()
        display.show()
        time.sleep(0.01)
    remote.unbind_all(il.register_input)


# program

if __name__ == "__main__":
    remote.start_pygame_thread()

    print("startup")
    start_dino()
    print("exited")

    remote.close_pygame_thread()
