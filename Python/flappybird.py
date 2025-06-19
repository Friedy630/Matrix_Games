import numpy as np
import time
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import game_library as game
import random as rng


class Pipe:
    def __init__(self, x, gap_y, gap_size=4):
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size

    def move(self):
        self.x -= 1

    def draw(self):
        for y in range(16):
            for x in range(self.x, self.x + 2):
                if not (self.gap_y <= y < self.gap_y + self.gap_size):
                    gl.set_pixel(x, y, gl.colors["green"])

    def is_off_screen(self):
        return self.x < -1

    def collides_with(self, bird_y):
        return not (self.gap_y <= bird_y < self.gap_y + self.gap_size)


class FlappyBirdGame(game.Game):
    def __init__(self):
        super().__init__()
        self.bird_y = 8
        self.bird_vy = 0
        self.gravity = 0.4
        self.flap_strength = self.gravity * -3
        self.pipes = []
        self.pipe_interval = 10
        self.pipe_gap = 5
        self.pipe_timer = 0
        self.score = 0
        self.spt = 0.1
        self.is_game_over = False
        self.pipe_prescale = 2

    def initialise(self):
        super().initialise()
        self.bird_y = 8
        self.bird_vy = 0
        self.pipes = []
        self.pipe_timer = 0
        self.score = 0
        self.is_game_over = False

    def update(self):
        if self.is_game_over:
            return

        # Input handling
        if il.inputs["space"] or il.inputs["up"]:
            self.bird_vy = self.flap_strength

        # Bird physics
        self.bird_vy += self.gravity
        self.bird_y += self.bird_vy
        self.bird_y = max(0, min(15, self.bird_y))

        if self.tick % self.pipe_prescale == 0:
            # Pipes
            if self.pipe_timer <= 0:
                gap_y = rng.randint(2, 16 - self.pipe_gap - 2)
                self.pipes.append(Pipe(16, gap_y, self.pipe_gap))
                self.pipe_timer = self.pipe_interval
            else:
                self.pipe_timer -= 1

            for pipe in self.pipes:
                pipe.move()
            self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        # Collision
        for pipe in self.pipes:
            if pipe.x == 2:
                if pipe.collides_with(int(round(self.bird_y))):
                    self.game_over()
            # Score
            if pipe.x == 1:
                self.score += 1

        # Out of bounds
        if self.bird_y >= 15:
            self.game_over()

    def render(self):
        gl.clear()
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()
        # Draw bird
        gl.set_pixel(2, int(round(self.bird_y)), gl.colors["yellow"])
        gl.show()

    def game_over(self):
        self.is_game_over = True
        print(f"Game Over! Score: {self.score}")


if __name__ == "__main__":
    from ulib import remote

    remote.start_pygame_thread()

    print("startup")
    flappy = FlappyBirdGame()
    flappy.initialise()
    flappy.play()
    print("exited")

    remote.close_pygame_thread()
