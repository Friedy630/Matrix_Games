inputs = {
    "left": False,
    "right": False,
    "down": False,
    "up": False,
    "space": False,
    "enter": False,
    "escape": False,
    "exit": False,
}


def register_input(key: str):
    global running
    if key in inputs:
        inputs[key] = True


def reset_inputs():
    for key in inputs:
        inputs[key] = False
