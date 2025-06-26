import numpy as np
import random as rng
import time
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import game_library as game

# Colors
snake_color = gl.colors["light_green"]
snake_head_color = gl.colors["green"]
fruit_color = gl.colors["red"]


class SnakeGame(game.Game):
    def __init__(
        self,
        snake_start_length=5,
        start_growth_factor=1.0,
        growth_factor_growth_factor=1.1,
        no_walls=False,
    ):
        super().__init__()
        self.snake_positions = [gl.Vec(7, 7)]
        self.snake_head_dir = gl.Vec(-1, 0)
        self.last_head_dir = gl.Vec(0, 0)
        self.snake_start_length = snake_start_length
        self.length_to_extend = snake_start_length
        self.start_growth_factor = start_growth_factor
        self.growth_factor = start_growth_factor
        self.growth_factor_growth_factor = growth_factor_growth_factor

        self.fruit_pos = gl.Vec(6, 6)

        self.no_walls = no_walls
        self.spt = 0.07
        self.walk_prescale = 6

    def initialise(self):
        super().initialise()
        self.snake_positions = [gl.Vec(7, 7)]
        self.snake_head_dir = gl.Vec(-1, 0)
        self.last_head_dir = gl.Vec(0, 0)
        self.length_to_extend = self.snake_start_length
        self.growth_factor = self.start_growth_factor
        self.fruit_pos = gl.Vec(6, 6)

        self.spawn_new_fruit()
        gl.set_pixel(
            self.snake_positions[0].x, self.snake_positions[0].y, snake_head_color
        )

    def spawn_new_fruit(self):
        while True:
            x = rng.randint(0, 15)
            y = rng.randint(0, 15)
            pos = gl.Vec(x, y)
            if pos not in self.snake_positions:
                self.fruit_pos = pos
                gl.set_pixel(self.fruit_pos.x, self.fruit_pos.y, fruit_color)
                break

    def update(self):
        # Steuerung
        if il.inputs["left"] and not 1 == self.last_head_dir.x:
            self.snake_head_dir = gl.Vec(-1, 0)
        if il.inputs["right"] and not -1 == self.last_head_dir.x:
            self.snake_head_dir = gl.Vec(1, 0)
        if il.inputs["up"] and not 1 == self.last_head_dir.y:
            self.snake_head_dir = gl.Vec(0, -1)
        if il.inputs["down"] and not -1 == self.last_head_dir.y:
            self.snake_head_dir = gl.Vec(0, 1)

        if self.tick % self.walk_prescale == 0:
            self.step_snake()

    def step_snake(self):
        current_head_pos = self.snake_positions[-1]
        new_head_pos = current_head_pos + self.snake_head_dir

        # Wand-Kollision
        if (
            new_head_pos.x < 0
            or new_head_pos.x >= 16
            or new_head_pos.y < 0
            or new_head_pos.y >= 16
        ):
            if self.no_walls:
                new_head_pos = gl.Vec(new_head_pos.x % 16, new_head_pos.y % 16)
            else:
                self.game_over()
                return

        # Selbst-Kollision
        if new_head_pos in self.snake_positions:
            self.game_over()
            return

        self.snake_positions.append(new_head_pos)

        # Frucht gegessen
        if new_head_pos == self.fruit_pos:
            self.length_to_extend += int(self.growth_factor)
            self.score += 1
            self.growth_factor *= self.growth_factor_growth_factor
            self.spawn_new_fruit()
        if self.length_to_extend <= 0:
            tail = self.snake_positions.pop(0)
            gl.set_pixel(tail.x, tail.y, gl.colors["background"])
        else:
            self.length_to_extend -= 1

        gl.set_pixel(new_head_pos.x, new_head_pos.y, snake_head_color)
        gl.set_pixel(current_head_pos.x, current_head_pos.y, snake_color)
        self.last_head_dir = self.snake_head_dir

    def render(self):
        gl.show()


if __name__ == "__main__":
    from ulib import remote

    remote.start_pygame_thread()

    print("startup")
    snake = SnakeGame()
    snake.initialise()
    snake.play()
    print("exited")

    remote.close_pygame_thread()
