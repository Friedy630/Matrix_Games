import pygame
import threading
import time
import numpy as np

# Einstellungen
WIDTH, HEIGHT = 16, 16
SCALE = 32

# Globals
pixels_cache = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
running = True
listening = False
window = None
window_ready = threading.Event()
flip = False

bindings = {}
all_binds = []

# Lock für Thread-Sicherheit
lock = threading.Lock()

def pygame_emu():
    global running, window, flip
    pygame.init()
    window = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    window_ready.set()
    should_close = False
    while running:
        if listening and not should_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    trigger_action("exit")
                    should_close = True
                elif event.type == pygame.KEYDOWN:
                    trigger_action(pygame.key.name(event.key))
        else:
            # Events trotzdem abholen, sonst blockiert pygame
            pygame.event.pump()
        if flip and not should_close:
            pygame.display.flip()
            flip = False
        time.sleep(0.01)
    pygame.quit()

# Starte Pygame Thread einmal
def start_pygame_thread():
    thread = threading.Thread(target=pygame_emu, daemon=True)
    thread.start()

def set_xy(x: int, y: int, color: tuple):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        with lock:
            pixels_cache[x, y] = color

def fill(color: tuple):
    with lock:
        pixels_cache[:, :] = color
    show()

def show():
    global window, flip
    window_ready.wait()
    with lock:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pygame.draw.rect(window, tuple(pixels_cache[x, y]), pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE))
    flip = True
    

def close():
    global running
    running = False

def trigger_action(key):
    for action in all_binds:
        action(key)
    if key in bindings:
        for action in bindings[key]:
            action(key)

def listen():
    global listening
    listening = True

def bind_key(key, action):
    if key not in bindings:
        bindings[key] = []
    bindings[key].append(action)

def unbind_key(key, action):
    if key in bindings and action in bindings[key]:
        bindings[key].remove(action)
        if not bindings[key]:
            del bindings[key]

def bind_all(action):
    all_binds.append(action)

def unbind_all(action):
    if action in all_binds:
        all_binds.remove(action)