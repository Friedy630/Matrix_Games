import numpy as np
import random as rng
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import game_library as game


class TetrisShape:
    def __init__(
        self, shape_matrix: np.ndarray, weight: int, color: tuple = gl.colors["white"]
    ):
        self.shape_matrix = shape_matrix
        self.weight = weight  # chance to spawn this shape
        self.position = gl.Vec(0, 0)  # position on the game field
        self.color = color  # color of the shape


def calculate_weights_sum(shape_set):
    """
    Calculates the sum of all weights in a shape set.
    """
    return sum(shape.weight for shape in shape_set)


exotic_color = gl.colors["grey"]  # color of any exotic shape

exotic_shapes = [
    TetrisShape(
        np.array(
            [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 1, 1],
                [0, 0, 1],
                [0, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 1],
                [0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 1],
                [0, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [1, 0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 1, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 1],
                [1, 1, 0],
                [0, 1, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 1, 1],
                [0, 0, 1],
                [0, 0, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
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
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 1, 1],
                [1, 1, 1, 0],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [0, 0, 0],
                [1, 1, 0],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
    TetrisShape(
        np.array(
            [
                [1, 0, 0],
                [1, 1, 1],
                [1, 1, 1],
            ]
        ).T,
        5,
        exotic_color,
    ),
]


exotic_weights_sum = calculate_weights_sum(exotic_shapes)


# Tetris Tetromino-Farben laut offizieller Guideline
shapes = [
    TetrisShape(
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
    TetrisShape(np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]]).T, 10, (0, 255, 0)),  # S
    TetrisShape(
        np.array([[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]).T,
        20,
        (0, 255, 255),
    ),  # I
    TetrisShape(np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]]).T, 15, (128, 0, 128)),
    TetrisShape(
        np.array(
            [
                [1, 1],
                [1, 1],
            ]
        ).T,
        15,
        (255, 255, 0),
    ),  # O
    TetrisShape(np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]]).T, 10, (255, 0, 0)),  # Z
    TetrisShape(np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]]).T, 15, (255, 165, 0)),  # L
]

weights_sum = calculate_weights_sum(shapes)


class TetrisGameShape:
    def __init__(self, shape_matrix: np.ndarray, weight: int, color: tuple):
        self.shape = TetrisShape(shape_matrix, weight, color)
        self.position = gl.Vec(0, 0)
        self.id = -1  # index in shape set

    def paste(self):
        gl.set_shape(self.shape.shape_matrix, self.position, self.shape.color)

    def cut(self):
        gl.set_shape(self.shape.shape_matrix, self.position, gl.colors["background"])

    def rotate(self, isleft: bool):
        rotated_matrix = gl.get_rotated_shape_matrix(self.shape.shape_matrix, isleft)
        self.cut()
        if gl.check_fit(rotated_matrix, self.position):
            self.shape.shape_matrix = rotated_matrix
        self.paste()

    def move_down(self):
        moved_position = self.position + gl.Vec(0, 1)
        self.cut()
        if not gl.check_fit(self.shape.shape_matrix, moved_position):
            self.paste()
            return False
        self.position = moved_position
        self.paste()
        return True

    def move_horizontal(self, isleft: bool):
        moved_position = self.position
        if isleft:
            moved_position += gl.Vec(-1, 0)
        else:
            moved_position += gl.Vec(1, 0)
        self.cut()
        if gl.check_fit(self.shape.shape_matrix, moved_position):
            self.position = moved_position
        self.paste()


class TetrisGame(game.Game):

    def __init__(
        self,
        spt=0.1,
        shapes=shapes,
        exotic_shapes=exotic_shapes,
        enable_acceleration=False,
        enable_exotic_shapes=False,
        exotic_shape_chance=0.3,
        enable_shape_weights=False,
        weights_sum=weights_sum,
        exotic_weights_sum=exotic_weights_sum,
    ):
        super().__init__()
        self.spt = spt
        self.fall_prescale = 10  # ticks per fall step
        self.current_shape = TetrisGameShape(np.zeros((3, 3)), 0, (255, 255, 255))
        self.side_to_side_pass = True

        # Exotic shapes
        self.enable_exotic_shapes = enable_exotic_shapes  # adds 20 more exiting shapes
        self.exotic_shape_chance = exotic_shape_chance  # chance to spawn an exotic shape instead of a normal one

        # Exotic Mechanics
        self.enable_acceleration = (
            enable_acceleration  # makes the falling speed accelerate over time
        )
        self.enable_shape_weights = (
            enable_shape_weights  # spawns each block with a given chance
        )

        self.shapes = shapes  # normal shapes
        self.exotic_shapes = exotic_shapes  # exotic shapes

        self.weights_sum = weights_sum  # sum of all normal shape weights
        self.exotic_weights_sum = exotic_weights_sum  # sum of all exotic shape weights

    def initialise(self):
        super().initialise()
        self.get_new_shape()

    def update(self):
        if not self.is_game_over:
            if self.tick % self.fall_prescale == 0:
                il.inputs["down"] = True
            if il.inputs["left"] != il.inputs["right"]:
                self.current_shape.move_horizontal(il.inputs["left"])
            if il.inputs["up"] != il.inputs["space"]:
                self.current_shape.rotate(il.inputs["up"])
            if il.inputs["down"] or il.inputs["enter"]:
                if not self.current_shape.move_down():
                    if self.current_shape.position.y < 0:
                        self.game_over()
                    else:
                        self.current_shape.paste()
                        self.check_for_full_row()
                        self.get_new_shape()

    def render(self):
        gl.show()

    def get_new_shape(self):
        self.current_shape.position = gl.Vec(6, -2)
        if self.enable_exotic_shapes and rng.random() <= self.exotic_shape_chance:
            if self.enable_shape_weights:
                self.set_shape(self.exotic_shapes, self.exotic_weights_sum)
            else:
                self.set_shape(self.exotic_shapes)
        else:
            if self.enable_shape_weights:
                self.set_shape(self.shapes, self.weights_sum)
            else:
                self.set_shape(self.shapes)
        self.current_shape.paste()
        if self.enable_acceleration:
            self.spt *= 0.98

    def set_shape(self, shape_set, weights_sum=None):
        while True:
            new_shape_id = (
                rng.randint(0, len(shape_set) - 1)
                if not weights_sum
                else self.get_loottable_hit(shape_set, weights_sum)
            )
            if new_shape_id != self.current_shape.id:
                self.current_shape.id = new_shape_id
                self.current_shape.shape = shape_set[new_shape_id]
                return

    def get_loottable_hit(self, weights_array, weights_sum):
        randInt = rng.randint(0, weights_sum - 1)
        w = 0
        i = -1  # shape_index
        while w < randInt:
            i += 1
            w += weights_array[i].weight
        return i

    def check_for_full_row(self):
        block_counter = 0
        local_score = 0
        score_multiplier = 0
        for row in range(16):
            for col in range(16):
                if tuple(gl.pixels[col, row]) != gl.colors["background"]:
                    block_counter += 1
            if block_counter == 16:
                self.remove_row(row)
                local_score += 100
                score_multiplier += 1
            block_counter = 0
        self.score += local_score * score_multiplier

    def remove_row(self, row: int):
        for y in range(row, 0, -1):
            for x in range(16):
                gl.set_pixel(x, y, gl.get_pixel(x, y - 1))


# main menu moved to main.py (future implementation for all games)


# program


if __name__ == "__main__":
    from ulib import remote

    remote.start_pygame_thread()

    print("startup")
    tetris = TetrisGame()
    tetris.initialise()
    tetris.play()
    tetris.stop()
    print("exited")

    remote.close_pygame_thread()
