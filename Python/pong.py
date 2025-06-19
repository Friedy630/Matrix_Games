import numpy as np
import time
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import game_library as game
import random as rng

# IDEAS:
# - boost for ball (rainbow animation)
# - ball speed increase over time


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.score = 0

    def move(self, direction):
        self.y += direction
        self.y = max(0, min(self.y, 16 - self.size))

    def draw(self):
        gl.set_shape(np.ones((1, self.size)), gl.Vec(self.x, self.y), gl.colors["grey"])


class Ball:
    def __init__(self, x, y):
        self.position = gl.Vec(x, y)
        self.direction = gl.Vec(1, 1)  # Initial direction
        self.reset()

    def move(self):
        if self.position.x == 0:
            self.direction = gl.Vec.zero()
            return -1
        elif self.position.x == 15:
            self.direction = gl.Vec.zero()
            return 1

        self.position += self.direction
        if self.position.y <= 0 or self.position.y >= 15:
            self.direction.y *= -1
        return 0

    def draw(self):
        gl.set_pixel(self.position.x, self.position.y, gl.colors["white"])

    def collide_with_paddle(self, paddle):
        # normal
        if (
            self.position.x == paddle.x - self.direction.x
            and paddle.y <= self.position.y < paddle.y + paddle.size
        ):
            self.direction.x *= -1
        # pointy
        if (
            self.position.x == paddle.x - self.direction.x
            and paddle.y - self.direction.y
            <= self.position.y
            < paddle.y + paddle.size - self.direction.y
        ):
            self.direction.x *= -1
            self.direction.y *= -1
        # oof
        if (
            self.position.x == paddle.x
            and paddle.y - self.direction.y
            <= self.position.y
            < paddle.y + paddle.size - self.direction.y
        ):
            self.direction.y *= -1

    def reset(self):
        self.position = gl.Vec(7, 7)
        self.direction = gl.Vec(1, 1)
        self.direction.x *= rng.choice([-1, 1])
        self.direction.y *= rng.choice([-1, 1])

    def point_animation(self, paddle, delay_time=0.5, iterations=2):
        color = gl.colors["red"] if paddle == 1 else gl.colors["blue"]
        delay = delay_time / (iterations * 2.0)
        for i in range(iterations):
            gl.set_pixel(self.position.x, self.position.y, color)
            gl.show()
            time.sleep(delay)
            gl.set_pixel(self.position.x, self.position.y, gl.colors["white"])
            gl.show()
            time.sleep(delay)


class PongGame(game.Game):
    def __init__(self, animated_ball=False):
        super().__init__()
        self.paddle_left = Paddle(1, 6)
        self.paddle_right = Paddle(14, 6)
        self.ball = Ball(7, 7)
        self.spt = 0.1
        self.ball_prescale = 6
        self.animated_ball = animated_ball

    def initialise(self):
        super().initialise()
        self.paddle_left = Paddle(1, 6)
        self.paddle_right = Paddle(14, 6)
        self.ball = Ball(7, 7)
        self.ball_timer = 0

    def update(self):
        # Steuerung
        if il.inputs["up"]:
            self.paddle_right.move(-1)
        if il.inputs["down"]:
            self.paddle_right.move(1)
        if il.inputs["w"]:
            self.paddle_left.move(-1)
        if il.inputs["s"]:
            self.paddle_left.move(1)

        point = 0
        if self.tick % self.ball_prescale == 0:
            self.ball.collide_with_paddle(self.paddle_left)
            self.ball.collide_with_paddle(self.paddle_right)
            point = self.ball.move()

        if point != 0:
            if point == -1:
                print("Right player scores!")
                self.paddle_right.score += 1
            elif point == 1:
                print("Left player scores!")
                self.paddle_left.score += 1
            self.ball.point_animation(point)
            self.ball.reset()

    def render(self):
        if self.animated_ball:
            gl.clear_column(1)
            gl.clear_column(14)
            gl.fade(0.7)
        else:
            gl.clear()

        self.paddle_left.draw()
        self.paddle_right.draw()
        self.ball.draw()

        gl.show()

    def stop(self):
        print(
            f"Game Over! Left Player: {self.paddle_left.score}, Right Player: {self.paddle_right.score}"
        )
        super().stop()


if __name__ == "__main__":
    from ulib import remote

    remote.start_pygame_thread()

    print("startup")
    pong = PongGame()
    pong.initialise()
    pong.play()
    print("exited")

    remote.close_pygame_thread()
