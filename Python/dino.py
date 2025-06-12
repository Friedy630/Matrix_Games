import numpy as np
import random as rng
from ulib import display, remote
import time
from ulib import graphics_library as gl
from ulib import input_library as il

is_game_over = False

walk_step_interval = 0.5


def restart():
    pass


def step_screen():
    pass


def start_dino():
    global snake_head_dir, running, length_to_extend, is_game_over
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
                snake_head_dir = gl.Vec(0, 1)
            time_ = time.time()
            if time_ - start_time >= walk_step_interval:
                start_time = time_
                step_screen()
        il.reset_inputs()
        display.show()
        time.sleep(0.1)
    remote.unbind_all(il.register_input)


# program

if __name__ == "__main__":
    remote.start_pygame_thread()

    print("startup")
    start_dino()
    print("exited")

    remote.close_pygame_thread()
