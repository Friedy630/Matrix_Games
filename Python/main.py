import time
import numpy as np
from ulib import graphics_library as gl
from ulib import input_library as il

import tetris
import snake
import pong

# icon chaos
tetris_icon = np.array(
    [
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["yellow"],
            gl.colors["yellow"],
            gl.colors["orange"],
            gl.colors["cyan"],
            gl.colors["white"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["yellow"],
            gl.colors["yellow"],
            gl.colors["orange"],
            gl.colors["cyan"],
            gl.colors["white"],
            gl.colors["white"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["orange"],
            gl.colors["orange"],
            gl.colors["cyan"],
            gl.colors["white"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["cyan"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["white"],
            gl.colors["white"],
        ],
        [
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["purple"],
            gl.colors["purple"],
            gl.colors["purple"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["purple"],
            gl.colors["blue"],
            gl.colors["background"],
            gl.colors["white"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["blue"],
            gl.colors["blue"],
            gl.colors["blue"],
            gl.colors["white"],
            gl.colors["background"],
        ],
    ]
)

snake_icon = np.array(
    [
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["light_green"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
    ]
)
pong_icon = np.array(
    [
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["grey"],
            gl.colors["grey"],
            gl.colors["grey"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["white"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            (4, 4, 4),
            gl.colors["background"],
            (48, 48, 48),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            (16, 16, 16),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["grey"],
            gl.colors["grey"],
            gl.colors["grey"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
    ]
)

# Arrow Shape
left_arrow_shape = np.array([[0, 1], [1, 0], [0, 1]]).T
right_arrow_shape = np.fliplr(left_arrow_shape.T).T
# list of games
games = [
    {"name": "TETRIS", "class": tetris.TetrisGame, "icon": tetris_icon},
    {"name": "SNAKE", "class": snake.SnakeGame, "icon": snake_icon},
    {"name": "PONG", "class": pong.PongGame, "icon": pong_icon},
]

# speed multipliers for game specific spt
speeds = [
    {"name": "SLOW", "value": 1.0, "color": gl.colors["green"]},
    {"name": "MEDIUM", "value": 0.75, "color": gl.colors["yellow"]},
    {"name": "FAST", "value": 0.5, "color": gl.colors["red"]},
]


def draw_menu(selected_game, selected_speed=0, with_arrows=True):
    gl.clear()
    # show game icon
    game_icon = games[selected_game]["icon"]
    for x in range(game_icon.shape[0]):
        for y in range(game_icon.shape[1]):
            color = game_icon[x, y]
            if not np.array_equal(color, gl.colors["background"]):
                gl.set_pixel(x + 4, y + 2, tuple(color))
    if with_arrows:
        gl.set_shape(left_arrow_shape, gl.Vec(1, 5), gl.colors["light_grey"])
        gl.set_shape(right_arrow_shape, gl.Vec(13, 5), gl.colors["light_grey"])
    draw_speed(selected_speed, False)
    gl.show()


# Create an array with only the outline ones (border of 1s, inside 0s)
speed_box = np.zeros((8, 3), dtype=int)
speed_box[0, :] = 1
speed_box[-1, :] = 1
speed_box[:, 0] = 1
speed_box[:, -1] = 1


def draw_speed(selected_speed, with_arrow=True):
    # Speed-Anzeige
    gl.clear_row(11)
    gl.clear_row(12)
    gl.clear_row(13)
    gl.set_shape(
        speed_box,
        gl.Vec(4, 11),
        gl.colors["light_grey"] if with_arrow else gl.colors["grey"],
    )
    for i, speed in enumerate(speeds):
        if i > selected_speed:
            break
        color = speed["color"]
        gl.set_shape(np.ones((2, 1)), gl.Vec(5 + i * 2, 12), color)
    if with_arrow:
        gl.set_pixel(3, 12, gl.colors["grey"])
        gl.set_pixel(12, 12, gl.colors["grey"])
    gl.show()


def main_menu():
    selected_game = 0
    running = True
    selected_speed = 0
    draw_menu(selected_game, selected_speed)
    while running:
        if il.inputs["exit"] or il.inputs["escape"]:
            return None, None
        if il.inputs["left"]:
            selected_game = (selected_game - 1) % len(games)
            draw_menu(selected_game, selected_speed)
        if il.inputs["right"]:
            selected_game = (selected_game + 1) % len(games)
            draw_menu(selected_game, selected_speed)
        if il.inputs["space"] or il.inputs["enter"]:
            il.reset_inputs()
            draw_menu(selected_game, selected_speed, False)
            selected_speed = speed_selection_menu(selected_speed)
            if selected_speed is not None:
                return selected_game, selected_speed
        il.reset_inputs()
        time.sleep(0.1)


def speed_selection_menu(selected_speed):
    running = True
    draw_speed(selected_speed)
    while running:
        if il.inputs["exit"] or il.inputs["escape"]:
            return None
        if il.inputs["left"]:
            selected_speed = max(selected_speed - 1, 0)
            draw_speed(selected_speed)
        if il.inputs["right"]:
            selected_speed = min(selected_speed + 1, len(speeds) - 1)
            draw_speed(selected_speed)
        if il.inputs["space"] or il.inputs["enter"]:
            return selected_speed
        il.reset_inputs()
        time.sleep(0.1)


def main():
    from ulib import remote

    remote.start_pygame_thread()
    il.initialise()
    while True:
        result = main_menu()
        if result == (None, None):
            break
        if result[1] is None:
            continue
        selected_game, selected_speed = result
        GameClass = games[selected_game]["class"]
        game_instance = GameClass()
        # Geschwindigkeit setzen, falls Attribut vorhanden
        if hasattr(game_instance, "spt"):
            game_instance.spt *= speeds[selected_speed]["value"]
        game_instance.initialise()
        game_instance.play()
    il.cleanup()
    remote.close_pygame_thread()


if __name__ == "__main__":
    main()


"""

diff1_step_interval_seconds = 1.0
diff2_step_interval_seconds = 0.75
diff3_step_interval_seconds = 0.5

# Shapes for menu
close_x_shape = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
space_shape = np.array([[1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1]])
space_shape = gl.get_rotated_shape_matrix(space_shape, True)
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
    gl.fill(gl.colors["black"])
    gl.set_shape(progress_bar_border_shape, gl.Vec(1, 1), gl.colors["grey"])
    gl.set_shape(progress_bar_inner_green_shape, gl.Vec(2, 2), gl.colors["green"])
    text_height = 6
    text_color = gl.colors["grey"]
    gl.set_shape(s_shape, gl.Vec(1, text_height), text_color)
    gl.set_shape(p_shape, gl.Vec(4, text_height), text_color)
    gl.set_shape(e_shape, gl.Vec(7, text_height), text_color)
    gl.set_shape(e_shape, gl.Vec(10, text_height), text_color)
    gl.set_shape(d_shape, gl.Vec(13, text_height), text_color)
    gl.show()
    while running:
        if il.inputs["escape"]:
            running = False
        if il.inputs["space"]:
            return True
        if il.inputs["exit"]:
            running = False
            return False
        if fall_step_interval_seconds == diff1_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(
                    progress_bar_inner_yellow_shape, gl.Vec(5, 2), gl.colors["yellow"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        if fall_step_interval_seconds == diff2_step_interval_seconds:
            if il.inputs["right"]:
                gl.set_shape(
                    progress_bar_inner_red_shape, gl.Vec(9, 2), gl.colors["red"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff3_step_interval_seconds
            if il.inputs["left"]:
                gl.set_shape(
                    progress_bar_inner_yellow_shape, gl.Vec(5, 2), gl.colors["black"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff1_step_interval_seconds
        if fall_step_interval_seconds == diff3_step_interval_seconds:
            if il.inputs["left"]:
                gl.set_shape(
                    progress_bar_inner_red_shape, gl.Vec(9, 2), gl.colors["black"]
                )
                gl.show()
                il.reset_inputs()
                fall_step_interval_seconds = diff2_step_interval_seconds
        il.reset_inputs()
        time.sleep(0.1)
    return False

"""
