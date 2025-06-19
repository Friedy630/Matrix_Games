import numpy as np
import time
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import display, remote, game_library as game

class GameOfLifeGame(game.Game):
    def __init__(self, blink_speed=0.3):
        super().__init__()
        self.virtual_screen = np.zeros((16, 16), dtype=int)
        self.cursor_pos = gl.Vec(0, 0)
        self.cursor_visible = True
        self.blink_speed = blink_speed
        self.blink_timer = 0
        self.in_setup_phase = True

    def initialise(self):
        gl.fill(gl.colors["background"])
        self.virtual_screen = np.zeros((16, 16), dtype=int)
        self.cursor_pos = gl.Vec(8, 8)
        self.in_setup_phase = True

    def update(self):
        if il.inputs["escape"] or il.inputs["exit"]:
            self.game_over()
            return

        if self.in_setup_phase:
            self.handle_setup_inputs()
        else:
            if il.inputs["space"] or il.inputs["enter"]:
                self.in_setup_phase = True
            else:
                self.compute_next_state()

    def render(self):
        gl.fill(gl.colors["background"])
        for x in range(16):
            for y in range(16):
                if self.virtual_screen[x, y] == 1:
                    gl.set_pixel(x, y, gl.colors["white"])

        if self.in_setup_phase and self.cursor_visible:
            gl.set_pixel(self.cursor_pos.x, self.cursor_pos.y, gl.colors["white"])
        gl.show()

    def handle_setup_inputs(self):
        if il.inputs["up"]:
            self.cursor_pos.y = max(0, self.cursor_pos.y - 1)
        elif il.inputs["down"]:
            self.cursor_pos.y = min(15, self.cursor_pos.y + 1)
        elif il.inputs["left"]:
            self.cursor_pos.x = max(0, self.cursor_pos.x - 1)
        elif il.inputs["right"]:
            self.cursor_pos.x = min(15, self.cursor_pos.x + 1)
        elif il.inputs["space"]:
            self.toggle_cell(self.cursor_pos.x, self.cursor_pos.y)
        elif il.inputs["enter"]:
            self.in_setup_phase = False
        elif il.inputs["escape"] or il.inputs["exit"]:
            self.game_over()

        self.cursor_visible = not self.cursor_visible if self.tick % 5 == 0 else self.cursor_visible

    def toggle_cell(self, x, y):
        self.virtual_screen[x, y] ^= 1

    def compute_next_state(self):
        new_screen = np.copy(self.virtual_screen)

        for x in range(16):
            for y in range(16):
                live_neighbors = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 16 and 0 <= ny < 16:
                            if self.virtual_screen[nx, ny] == 1:
                                live_neighbors += 1

                if self.virtual_screen[x, y] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_screen[x, y] = 0
                elif live_neighbors == 3:
                    new_screen[x, y] = 1

        self.virtual_screen = new_screen
        time.sleep(0.2)

# Programmstart
if __name__ == "__main__":
    remote.start_pygame_thread()
    print("startup")
    game = GameOfLife()
    game.initialise()
    game.play()
    game.stop()
    print("exited")
    remote.close_pygame_thread()
