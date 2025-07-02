import numpy as np
import time
from ulib import graphics_library as gl
from ulib import input_library as il
from ulib import display, remote, game_library as game


class GameOfLifeGame(game.Game):
    def __init__(self, blink_speed=0.3, spt=0.2):
        super().__init__()
        self.grid_size      = 100
        self.view_size      = 16
        self.offset         = (self.grid_size - self.view_size) // 2
        self.virtual_screen = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.cursor_pos     = gl.Vec(7, 7)
        self.cursor_visible = True
        self.blink_speed    = blink_speed
        self.spt            = spt
        self.in_setup_phase = True
        self.paused         = False
        self.iterations     = 0
        self.score          = 0

    def initialise(self):
        gl.fill(gl.colors["background"])
        self.virtual_screen.fill(0)
        self.cursor_pos     = gl.Vec(7, 7)
        self.cursor_visible = True
        self.in_setup_phase = True
        self.paused         = False
        self.iterations     = 0
        self.score          = 0

    def update(self):
        if il.inputs["escape"] or il.inputs["exit"]:
            self.game_over()
            return

        if self.in_setup_phase and self.tick % max(1, int(self.blink_speed / self.spt)) == 0:
            self.cursor_visible = not self.cursor_visible

        if self.in_setup_phase:
            self.handle_setup_inputs()
        else:
            if il.inputs["enter"]:
                self.in_setup_phase = True
                self.paused = False
                il.reset_inputs()
                return

            if il.inputs["space"]:
                self.paused = not self.paused
                il.reset_inputs()
                return

            if not self.paused:
                old_screen = self.virtual_screen
                self.compute_next_state()
                self.iterations += 1
                self.score = self.iterations

                if np.array_equal(old_screen, self.virtual_screen):
                    self.paused = True
                    print(f"Stabiler Zustand erreicht – Score: {self.score}")
                    # Kein self.stop(), kein Rücksprung – Benutzer darf ESC drücken
                    return

        il.reset_inputs()

    def render(self):
        gl.clear(override=False)
        # Sichtbaren 16×16-Ausschnitt zeichnen
        for x in range(self.view_size):
            for y in range(self.view_size):
                gx, gy = x + self.offset, y + self.offset
                if self.virtual_screen[gx, gy] == 1:
                    gl.set_pixel(x, y, gl.colors["white"])

        # Cursor anzeigen, aber nur in Setup-Phase
        if self.in_setup_phase:
            cx, cy = self.cursor_pos.x, self.cursor_pos.y
            if self.cursor_visible:
                gl.set_pixel(cx, cy, gl.colors["white"])
            else:
                gl.set_pixel(cx, cy, gl.colors["background"])

        gl.show()

    def handle_setup_inputs(self):
        moved  = False
        old_pos = self.cursor_pos

        if il.inputs["up"]:
            self.cursor_pos.y = max(0, self.cursor_pos.y - 1)
            moved = True
        elif il.inputs["down"]:
            self.cursor_pos.y = min(self.view_size - 1, self.cursor_pos.y + 1)
            moved = True
        elif il.inputs["left"]:
            self.cursor_pos.x = max(0, self.cursor_pos.x - 1)
            moved = True
        elif il.inputs["right"]:
            self.cursor_pos.x = min(self.view_size - 1, self.cursor_pos.x + 1)
            moved = True

        if moved:
            self.restore_previous_cursor_pixel(old_pos.x, old_pos.y)
            self.cursor_visible = True
            il.reset_inputs()
            return

        if il.inputs["space"]:
            self.toggle_cell(self.cursor_pos.x, self.cursor_pos.y)
            il.reset_inputs()
            return

        if il.inputs["enter"]:
            self.in_setup_phase = False
            il.reset_inputs()
            return

    def toggle_cell(self, x, y):
        gx, gy = x + self.offset, y + self.offset
        self.virtual_screen[gx, gy] ^= 1

    def restore_previous_cursor_pixel(self, x, y):
        gx, gy = x + self.offset, y + self.offset
        if self.virtual_screen[gx, gy] == 1:
            gl.set_pixel(x, y, gl.colors["white"])
        else:
            gl.set_pixel(x, y, gl.colors["background"])

    def compute_next_state(self):
        new_screen = self.virtual_screen.copy()
        # Conway’s Game of Life über gesamte 100×100-Matrix
        for x in range(1, self.grid_size - 1):
            for y in range(1, self.grid_size - 1):
                live_neighbors = (
                    np.sum(self.virtual_screen[x-1:x+2, y-1:y+2])
                    - self.virtual_screen[x, y]
                )
                if self.virtual_screen[x, y] == 1:
                    new_screen[x, y] = 1 if 2 <= live_neighbors <= 3 else 0
                else:
                    new_screen[x, y] = 1 if live_neighbors == 3 else 0

        self.virtual_screen = new_screen
        time.sleep(self.spt)


if __name__ == "__main__":
    #remote.start_pygame_thread()
    print("startup")
    game = GameOfLifeGame()
    game.initialise()
    game.play()
    game.stop()
    print("exited")
    #remote.close_pygame_thread()
