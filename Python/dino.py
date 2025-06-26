import numpy as np
import random as rng
from ulib import remote, game_library as game
import time
from ulib import graphics_library as gl
from ulib import input_library as il

class Dino(game.Game):
    def __init__(self):
        super().__init__()
        self.max_jmp_height = 5
        self.jump_height = 0
        self.base_height = 4

        self.player_pos = gl.Vec(2, 5)

        self.obs_spawn_interval_min = 0.6     # in seconds
        self.obs_spawn_interval_max = 1.3     # in seconds

        self.ground_color = gl.colors["green"]
        self.player_color = gl.colors["red"]
        self.obstacle_color = gl.colors["white"]

        # clock 1: player redraw clock
        self.last_player_step_time = 0.0
        self.player_step_interval = 0.01

        # clock 2: jump clock, so a jump cannot start when one is already in progress
        self.last_jump_time = 0.0
        self.jump_duration = 0.7

        # gets set to true, if jump is pressed right before the jump ends; "forgiving controls"
        self.jump_directly = False

        # clock 3: world redraw clock
        self.last_world_step_time = 0.0
        self.world_step_interval = 0.05

        # clock 4: obstacle spawn clock
        self.last_spawn_time = 0.0
        self.spawn_interval = 1

        self.player_shape = np.array(
        [
            [1, 1],
            [1, 1],
        ])

        self.spt = 0.01

        self.obstacles = [
            np.array([
                [0, 0],
                [0, 0],
                [1, 1],
                [1, 1],
                [1, 1]
            ]).T,
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [1, 1],
                [1, 1]
            ]).T,
            np.array([
                [0, 0],
                [0, 0],
                [0, 1],
                [1, 1],
                [1, 1]
            ]).T,
            np.array([
                [0, 0],
                [0, 0],
                [0, 1],
                [1, 0],
                [0, 1]
            ]).T,
            np.array([
                [0, 1],
                [1, 1],
                [0, 1],
                [0, 0],
                [0, 0],
            ]).T
        ]

        self.obstacle_instances : list[tuple[gl.Vec, int]] = []

    def player_clock_step(self, current_time):
        if current_time - self.last_player_step_time >= self.player_step_interval:
            self.last_player_step_time = current_time
            self.player_step(current_time)


    def on_jump(self, current_time):
        delta_time = current_time - self.last_jump_time
        if delta_time >= self.jump_duration:
            self.last_jump_time = current_time
            self.jump_directly = False
        elif self.jump_duration - delta_time <= 0.1:
            self.jump_directly = True


    def world_clock_step(self, current_time):
        if current_time - self.last_world_step_time >= self.world_step_interval:
            self.last_world_step_time = current_time
            self.world_step()


    def spawn_clock_step(self, current_time):
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = current_time
            self.spawn_step()#


    def player_step(self, current_time):
        if not self.check_fit(self.player_shape, self.player_pos):
            self.is_game_over = True
        gl.set_shape(self.player_shape, self.player_pos, gl.colors["background"])
        jump_height = max(0, self.max_jmp_height * (-(4 / (self.jump_duration**2)) * (((current_time - self.last_jump_time) - (self.jump_duration / 2))**2) + 1))
        self.player_pos.y = 16 - round(jump_height) - self.base_height - 2
        if not self.check_fit(self.player_shape, self.player_pos):
            self.is_game_over = True
        gl.set_shape(self.player_shape, self.player_pos, self.player_color)
        if self.is_game_over:
            self.world_draw()


    def check_fit(self, shape_matrix: np.ndarray, position: gl.Vec):
        for x in range(shape_matrix.shape[0]):
            for y in range(shape_matrix.shape[1]):
                color = gl.get_pixel(position.x + x, position.y + y)
                if (
                    shape_matrix[x, y] == 1
                    and (color != gl.colors["background"] and color != self.player_color)
                ):
                    return False
        return True
    

    def world_step(self):
        for obst in self.obstacle_instances:
            gl.set_shape(self.obstacles[obst[1]], obst[0], gl.colors["background"])
        for obst in self.obstacle_instances:
            obst[0].x -= 1
        self.world_draw()

    def world_draw(self):
        for obst in self.obstacle_instances:
            gl.set_shape(self.obstacles[obst[1]], obst[0], self.obstacle_color)


    def spawn_step(self):
        self.obstacle_instances.append((gl.Vec(16, 16 - self.base_height - 5), rng.randint(0, len(self.obstacles) - 1)))
        self.spawn_interval = self.obs_spawn_interval_min + rng.random() * (self.obs_spawn_interval_max - self.obs_spawn_interval_min)


    def initialise(self):
        for obst in self.obstacle_instances:
            gl.set_shape(self.obstacles[obst[1]], obst[0], gl.colors["background"])
        self.obstacle_instances.clear()
        super().initialise()
        for y in range(self.base_height + 1):
            for x in range(16):
                gl.set_pixel(x, 16 - y, self.ground_color)


    def update(self):
        current_time = time.time()
        if il.inputs["up"] or self.jump_directly:
            self.on_jump(current_time)
        self.player_clock_step(current_time)
        self.world_clock_step(current_time)
        self.spawn_clock_step(current_time)

    def render(self):
        gl.show()


# program

if __name__ == "__main__":
    remote.start_pygame_thread()

    print("startup")
    dino = Dino()
    dino.initialise()
    dino.play()
    print("exited")

    remote.close_pygame_thread()
