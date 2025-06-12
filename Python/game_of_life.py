import numpy as np
import random as rng
from ulib import display, remote
import time
from ulib import graphics_library as gl
from ulib import input_library as il
import threading


cursor_position = gl.Vec(0, 0)
clock_cycle = 0
running = False
cursor_visible = True
blink_speed = 0.3
virtual_screen = np.zeros((16, 16), dtype=int)


def clear_temp_pixels():
    global virtual_screen
    for x in range(16):
        for y in range(16):
            if virtual_screen[x, y] == -1:
                gl.setpixel(x, y, gl.colors["background"])
                virtual_screen[x, y] = 0


def screen_setlastingpixel(x: int, y: int, value: int):
    global virtual_screen
    if 0 <= x < 16 and 0 <= y < 16:
        virtual_screen[x, y] = value
        if value == 0:
            gl.setpixel(x, y, gl.colors["background"])
        else:
            gl.setpixel(x, y, gl.colors["white"])


def blink_cursor():
    global cursor_visible, running, blink_speed
    while running:
        cursor_visible = not cursor_visible
        time.sleep(blink_speed)


def real_game_of_life_algorithm():
    global virtual_screen, running
    while running:
        new_screen = np.copy(virtual_screen)

        for x in range(16):
            for y in range(16):
                live_neighbors = 0

                # Count live neighbors
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 16 and 0 <= ny < 16:
                            if virtual_screen[nx, ny] == 1:
                                live_neighbors += 1

                # Apply Game of Life rules
                if virtual_screen[x, y] == 1 and (
                    live_neighbors < 2 or live_neighbors > 3
                ):
                    new_screen[x, y] = 0
                elif virtual_screen[x, y] == 0 and live_neighbors == 3:
                    new_screen[x, y] = 1
                else:
                    new_screen[x, y] = virtual_screen[x, y]

        # Update the display
        for x, y in np.ndindex(virtual_screen.shape):
            if virtual_screen[x, y] == 1:
                gl.setpixel(x, y, gl.colors["white"])
            else:
                gl.setpixel(x, y, gl.colors["background"])

        display.show()
        if il.inputs["space"] or il.inputs["enter"]:
            if running:
                print("Game of Life paused")
                running = False
            else:
                print("Game of Life resumed")
                running = True

        if il.inputs["exit"] or il.inputs["escape"]:
            running = False
            break

        il.reset_inputs()

        # Update the virtual screen
        virtual_screen = new_screen

        time.sleep(0.5)


def game_of_life_selection():
    global cursor_position
    global clock_cycle
    global running

    print("Game of Life starting...")
    gl.fill(gl.colors["background"])
    display.show()
    print("Game of Life started")
    screen_setlastingpixel(8, 8, 1)

    while running:

        for x in range(16):
            for y in range(16):
                if virtual_screen[x, y] == 1:
                    gl.setpixel(x, y, gl.colors["white"])
                else:
                    gl.setpixel(x, y, gl.colors["background"])

        if il.inputs["exit"] or il.inputs["escape"]:
            running = False
            break
        elif il.inputs["up"]:
            cursor_position.y = max(0, cursor_position.y - 1)
            clear_temp_pixels()
        elif il.inputs["down"]:
            cursor_position.y = min(15, cursor_position.y + 1)
            clear_temp_pixels()
        elif il.inputs["left"]:
            cursor_position.x = max(0, cursor_position.x - 1)
            clear_temp_pixels()
        elif il.inputs["right"]:
            cursor_position.x = min(15, cursor_position.x + 1)
            clear_temp_pixels()
        elif il.inputs["space"]:
            if virtual_screen[cursor_position.x, cursor_position.y] != 1:
                screen_setlastingpixel(cursor_position.x, cursor_position.y, 1)
            else:
                screen_setlastingpixel(cursor_position.x, cursor_position.y, 0)
        elif il.inputs["enter"]:
            print("Starting Game of Life...")
            break

        il.reset_inputs()

        if virtual_screen[cursor_position.x, cursor_position.y] == 1:
            if cursor_visible:
                gl.setpixel(cursor_position.x, cursor_position.y, gl.colors["white"])
            else:
                gl.setpixel(
                    cursor_position.x, cursor_position.y, gl.colors["background"]
                )
        else:
            if cursor_visible:
                gl.setpixel(cursor_position.x, cursor_position.y, gl.colors["white"])
                virtual_screen[cursor_position.x, cursor_position.y] = -1
            else:
                gl.setpixel(
                    cursor_position.x, cursor_position.y, gl.colors["background"]
                )
                virtual_screen[cursor_position.x, cursor_position.y] = 0

        clock_cycle += 1
        display.show()
        time.sleep(0.1)

    print("Game of Life preparation finished")


def main():
    global cursor_position
    global clock_cycle
    global running
    global virtual_screen

    virtual_screen = np.zeros((16, 16), dtype=int)

    il.initialise()
    running = True
    blink_thread = threading.Thread(target=blink_cursor, daemon=True)
    blink_thread.start()
    clock_cycle = 0
    game_of_life_selection()
    il.reset_inputs()
    real_game_of_life_algorithm()
    running = False
    il.cleanup()
    gl.fill(gl.colors["background"])


remote.start_pygame_thread()

print("startup")
main()
print("exited")

remote.close_pygame_thread()
