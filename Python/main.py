import time
import numpy as np
from ulib import graphics_library as gl
from ulib import input_library as il

import tetris
import snake
import pong
import flappybird
import game_of_life
import dino;

# icon chaos
tetris_icon = np.array(
    [
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["yellow"],
            gl.colors["yellow"],
            gl.colors["orange"],
            gl.colors["cyan"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["yellow"],
            gl.colors["yellow"],
            gl.colors["orange"],
            gl.colors["cyan"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["orange"],
            gl.colors["orange"],
            gl.colors["cyan"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["cyan"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
        ],
        [
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["purple"],
            gl.colors["purple"],
            gl.colors["purple"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["purple"],
            gl.colors["blue"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["blue"],
            gl.colors["blue"],
            gl.colors["blue"],
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

flappybird_icon = np.array(
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
            gl.colors["yellow"],
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
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["green"],
        ],
        [
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["green"],
            gl.colors["green"],
        ],
        [
            (0, 16, 0),
            (0, 16, 0),
            gl.colors["background"],
            gl.colors["background"],
            (0, 16, 0),
            (0, 16, 0),
            (0, 16, 0),
            (0, 16, 0),
        ],
        [
            (0, 2, 0),
            (0, 2, 0),
            gl.colors["background"],
            gl.colors["background"],
            (0, 2, 0),
            (0, 2, 0),
            (0, 2, 0),
            (0, 2, 0),
        ],
    ]
)

dino_icon = np.array(
    [
        [
            gl.colors["background"],
            gl.colors["background"],
            (20, 20, 20),
            (61, 61, 61),
            (82, 82, 82),
            (20, 20, 20),
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            (82, 82, 82),
            (61, 61, 61),
            (20, 20, 20),
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            (20, 20, 20),
            (82, 82, 82),
            (82, 82, 82),
            (82, 82, 82),
            (61, 61, 61),
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            (20, 20, 20),
            (82, 82, 82),
            (82, 82, 82),
            (82, 82, 82),
            (61, 61, 61),
            gl.colors["background"],
        ],
        [
            (41, 41, 41),
            (82, 82, 82),
            (82, 82, 82),
            (82, 82, 82),
            (82, 82, 82),
            (82, 82, 82),
            (41, 41, 41),
            (61, 61, 61),
        ],
        [
            (82, 82, 82),
            (82, 82, 82),
            (61, 61, 61),
            (61, 61, 61),
            (41, 41, 41),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            (82, 82, 82),
            (82, 82, 82),
            (41, 41, 41),
            (20, 20, 20),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            (61, 61, 61),
            (82, 82, 82),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
    ]
)

game_of_life_icon = np.array(
    [
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
            gl.colors["background"],
            gl.colors["white"],
            gl.colors["background"],
            gl.colors["white"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["white"],
            gl.colors["white"],
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
            gl.colors["white"],
            gl.colors["white"],
            gl.colors["white"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["white"],
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
            gl.colors["white"],
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
    {
        "name": "FLAPPY BIRD",
        "class": flappybird.FlappyBirdGame,
        "icon": flappybird_icon,
    },
    {"name": "DINO", "class": dino.DinoGame, "icon": dino_icon},
    {
        "name": "GAME OF LIFE",
        "class": game_of_life.GameOfLifeGame,
        "icon": game_of_life_icon,
    }
]

# speed multipliers for game specific spt
speeds = [
    {"name": "SLOW", "value": 1.5, "color": gl.colors["green"]},
    {"name": "MEDIUM", "value": 1.0, "color": gl.colors["yellow"]},
    {"name": "FAST", "value": 0.5, "color": gl.colors["red"]},
]


def draw_menu(selected_game, selected_speed=0, with_arrows=True):
    gl.clear()
    # show game icon
    game_icon = games[selected_game]["icon"]
    gl.draw_image(game_icon, 4, 2)
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
            selected_speed, selected = speed_selection_menu(selected_speed)
            if selected:
                return selected_game, selected_speed
            draw_menu(selected_game, selected_speed)
        il.reset_inputs()
        time.sleep(0.05)


def speed_selection_menu(selected_speed):
    running = True
    draw_speed(selected_speed)
    while running:
        if il.inputs["exit"] or il.inputs["escape"]:
            return selected_speed, False
        if il.inputs["left"]:
            selected_speed = max(selected_speed - 1, 0)
            draw_speed(selected_speed)
        if il.inputs["right"]:
            selected_speed = min(selected_speed + 1, len(speeds) - 1)
            draw_speed(selected_speed)
        if il.inputs["space"] or il.inputs["enter"]:
            return selected_speed, True
        il.reset_inputs()
        time.sleep(0.05)


end_screen = np.array(
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            (4, 4, 4),
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
        ],
        [
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["background"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["red"],
            gl.colors["red"],
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
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
            gl.colors["background"],
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


def main():
    from ulib import remote

    remote.start_pygame_thread()
    gl.brightness = 32
    il.initialise()
    while True:
        result = main_menu()
        if result == (None, None):
            gl.clear()
            gl.draw_image(end_screen, 0, 0)
            gl.show()
            break
        if result[1] is None:
            continue
        selected_game, selected_speed = result
        GameClass = games[selected_game]["class"]
        game_instance = GameClass()
        game_instance.set_difficulty(selected_speed, speeds[selected_speed]["value"])
        game_instance.initialise()
        game_instance.play()
    il.cleanup()
    remote.close_pygame_thread()


if __name__ == "__main__":
    main()