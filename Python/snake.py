import numpy as np
import random as rng
from ulib import display, remote
import time
from ulib import graphics_library as gl
from ulib import input_library as il

#### settings

snake_start_length = 5

walk_step_interval = 0.3

start_growth_factor = 1.0

growth_factor_groth_factor = 1.1

snake_color = gl.colors["light_green"]

snake_head_color = gl.colors["green"]

background_color = gl.colors["black"]

fruit_color = gl.colors["red"]

no_walls = False

####

fruit_pos = gl.Vec(6, 6)

growth_factor = 1.0

snake_positions = [gl.Vec(7, 7)]

snake_head_dir = gl.Vec(-1, 0)

last_head_dir = gl.Vec(0, 0)

running = True

length_to_extend = 0

score = 0

is_game_over = False


def spawn_new_fruit():
    global fruit_pos
    while fruit_pos in snake_positions:
        x = rng.randint(0, 15)
        y = rng.randint(0, 15)
        fruit_pos = gl.Vec(x, y)
    gl.setpixel(fruit_pos.x, fruit_pos.y, fruit_color)


def game_over():
    global is_game_over
    print("game over")
    is_game_over = True


def step_snake():
    global snake_positions, length_to_extend, score, growth_factor, last_head_dir
    current_head_pos = snake_positions[len(snake_positions) - 1]
    new_head_pos = current_head_pos + snake_head_dir
    if (
        new_head_pos.x < 0
        or new_head_pos.x >= 16
        or new_head_pos.y < 0
        or new_head_pos.y >= 16
    ):
        if no_walls:
            new_head_pos = gl.Vec(new_head_pos.x % 16, new_head_pos.y % 16)
        else:
            game_over()
    if new_head_pos in snake_positions:
        game_over()
    snake_positions.append(new_head_pos)
    if new_head_pos == fruit_pos:
        length_to_extend += int(growth_factor)
        score += 1
        growth_factor *= growth_factor_groth_factor
        spawn_new_fruit()
    if length_to_extend <= 0:
        gl.setpixel(snake_positions[0].x, snake_positions[0].y, background_color)
        snake_positions.remove(snake_positions[0])
    else:
        length_to_extend -= 1
    gl.setpixel(new_head_pos.x, new_head_pos.y, snake_head_color)
    gl.setpixel(current_head_pos.x, current_head_pos.y, snake_color)
    last_head_dir = snake_head_dir


def restart():
    print("start")
    global snake_head_dir, length_to_extend, is_game_over, snake_positions, growth_factor
    gl.fill(background_color)
    snake_positions = [gl.Vec(7, 7)]
    growth_factor = start_growth_factor
    gl.setpixel(snake_positions[0].x, snake_positions[0].y, snake_head_color)
    length_to_extend = snake_start_length
    spawn_new_fruit()
    is_game_over = False


def start_snake():
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
            if il.inputs["left"] and not 1 == last_head_dir.x:
                snake_head_dir = gl.Vec(-1, 0)
            if il.inputs["right"] and not -1 == last_head_dir.x:
                snake_head_dir = gl.Vec(1, 0)
            if il.inputs["up"] and not 1 == last_head_dir.y:
                snake_head_dir = gl.Vec(0, -1)
            if il.inputs["down"] and not -1 == last_head_dir.y:
                snake_head_dir = gl.Vec(0, 1)
            time_ = time.time()
            if time_ - start_time >= walk_step_interval:
                start_time = time_
                step_snake()
        il.reset_inputs()
        display.show()
        time.sleep(0.1)
    remote.unbind_all(il.register_input)


# program

remote.start_pygame_thread()

print("startup")
start_snake()
print("exited")

remote.close_pygame_thread()
