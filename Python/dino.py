import numpy as np
import random as rng
from ulib import display, remote
import time
from ulib import graphics_library as gl
from ulib import input_library as il

is_game_over = False

walk_step_interval = 0.01

def restart():
    pass

max_jmp_height = 8
last_jump_time = 0
jump_duration = 0.5
jump_height = 0
base_height = 5

player_pos = gl.Vec(2, 5)

obs_spawn_pause_min = 1     # in seconds
obs_spawn_pause_max = 2     # in seconds

last_spawn_time = 0

spawn_pause = 0

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
    ]),
    np.array([
        [0, 0],
        [1, 1],
        [1, 1]
    ]),
    np.array([
        [0, 1],
        [1, 1],
        [1, 1]
    ]),
    np.array([
        [0, 1],
        [1, 0],
        [0, 1]
    ]),
]

obstacles_positions = []


def step_screen():
    global jump_height
    delta_time = time.time() - last_jump_time
    if delta_time < jump_duration:
        jump_height = jmp_formula(delta_time / jump_duration)
    else:
        jump_height = 0
    gl.set_shape(player_shape, player_pos, gl.colors["background"])
    player_pos.y = 16 - round(jump_height) - base_height
    gl.set_shape(player_shape, player_pos, gl.colors["red"])

def jmp_formula(x):
    a = jump_duration
    return  max_jmp_height * (-1/(a**2)*(x-a)**2 + 1)

def on_jump():
    global last_jump_time
    _time = time.time()
    if _time - last_jump_time >= jump_duration:
        last_jump_time = time.time()

def spawn_tick():
    global spawn_pause, last_spawn_time
    _time = time.time()
    time_since_last_spawn = _time - last_spawn_time
    if time_since_last_spawn < spawn_pause:
        return
    obstacles_positions.append(16)
    spawn_pause = obs_spawn_pause_min + rng.random() * (obs_spawn_pause_max - obs_spawn_pause_min)
    last_spawn_time = _time
        

def start_dino():
    global running, is_game_over, last_jump_time
    running = True
    restart()
    il.initialise()
    for y in range(base_height - 1):
        for x in range(16):
            gl.set_pixel(x, 16 - y, gl.colors["green"])
    start_time = time.time()
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
            if il.inputs["up"]:
                on_jump()
            time_ = time.time()
            if time_ - start_time >= walk_step_interval:
                start_time = time_
                print("tick")
                step_screen()
                spawn_tick()
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
