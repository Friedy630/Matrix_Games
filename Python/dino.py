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

player_shape = np.array(
    [
        [1, 1],
        [1, 1],
    ])

def step_screen():
    global jump_height
    delta_time = time.time() - last_jump_time
    if delta_time < jump_duration:
        jump_height = jmp_formula(delta_time / jump_duration);
    else:
        jump_height = 0
    gl.set_shape(player_shape, player_pos, gl.colors["background"])
    player_pos.y = 16 - round(jump_height) - base_height
    gl.set_shape(player_shape, player_pos, gl.colors["green"])

def jmp_formula(x):
    a = jump_duration
    return  max_jmp_height * (-1/(a**2)*(x-a)**2 + 1)

def on_jump():
    global last_jump_time
    _time = time.time()
    if _time - last_jump_time >= jump_duration:
        last_jump_time = time.time()

def start_dino():
    global running, is_game_over, last_jump_time
    running = True
    restart()
    il.initialise()
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
