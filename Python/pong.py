import numpy as np
from ulib import graphics_library as gl
from ulib import input_library as il
import time


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 4
        self.score = 0

    def move(self, direction):
        self.y += direction

    def draw(self):
        gl.set_shape(np.ones((1, self.size)), gl.Vec(self.x, self.y), gl.colors["grey"])

    def clear(self):
        gl.set_shape(
            np.ones((1, self.size)), gl.Vec(self.x, self.y), gl.colors["background"]
        )


class Ball:
    def __init__(self, x, y):
        self.position = gl.Vec(x, y)
        self.direction = gl.Vec(1, 1)  # Initial direction

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
        gl.setpixel(self.position.x, self.position.y, gl.colors["white"])

    def clear(self):
        gl.setpixel(self.position.x, self.position.y, gl.colors["background"])

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
            and paddle.y - 1 <= self.position.y < paddle.y + paddle.size + 1
        ):
            self.direction.y *= -1

    def reset(self):
        self.position = gl.Vec(7, 7)
        self.direction = gl.Vec(1, 1)

    def point_animation(self, paddle, delay_time):
        color = gl.colors["red"] if paddle == 1 else gl.colors["blue"]
        iterations = 2
        delay = delay_time / (iterations * 2.0)
        for i in range(iterations):
            gl.setpixel(self.position.x, self.position.y, color)
            gl.show()
            time.sleep(delay)
            gl.setpixel(self.position.x, self.position.y, gl.colors["white"])
            gl.show()
            time.sleep(delay)


running = False
paddle_left = Paddle(1, 6)
paddle_right = Paddle(14, 6)
ball = Ball(7, 7)


def restart():
    print("Starting Pong...")
    global paddle_left, paddle_right, ball
    paddle_left = Paddle(1, 6)
    paddle_right = Paddle(14, 6)
    ball = Ball(7, 7)


def play():
    global running
    running = True
    restart()
    il.initialise()
    ball_timer = 0
    while running:
        paddle_left.clear()
        paddle_right.clear()

        if il.inputs["up"]:
            paddle_right.move(-1)
        if il.inputs["down"]:
            paddle_right.move(1)
        if il.inputs["w"]:
            paddle_left.move(-1)
        if il.inputs["s"]:
            paddle_left.move(1)
        if il.inputs["exit"]:
            running = False
            return False
        if il.inputs["escape"]:
            running = False

        paddle_left.draw()
        paddle_right.draw()

        ball.clear()
        if ball_timer % 4 == 0:
            ball.collide_with_paddle(paddle_left)
            ball.collide_with_paddle(paddle_right)
            point = ball.move()

        ball.draw()

        if point != 0:
            if point == -1:
                print("Right player scores!")
                paddle_right.score += 1
            elif point == 1:
                print("Left player scores!")
                paddle_left.score += 1
            ball.point_animation(point, 0.5)
            ball.clear()
            ball.reset()
            ball_timer = -1

        il.reset_inputs()
        gl.show()
        time.sleep(0.05)
        ball_timer += 1
    il.cleanup()


if __name__ == "__main__":
    from ulib import remote

    remote.start_pygame_thread()

    print("startup")
    play()
    print("exited")

    remote.close_pygame_thread()
