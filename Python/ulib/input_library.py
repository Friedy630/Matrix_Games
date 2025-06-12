from ulib import remote

inputs = {
    "left": False,
    "right": False,
    "down": False,
    "up": False,
    "space": False,
    "enter": False,
    "return": False,
    "escape": False,
    "exit": False,
    "esc": False,
    "w": False,
    "a": False,
    "s": False,
    "d": False,
}


def register_input(key: str):
    key = key.lower()
    if key in inputs:
        inputs[key] = True
        if key == "esc":
            inputs["escape"] = True
        if key == "return":
            inputs["enter"] = True


def reset_inputs():
    for key in inputs:
        inputs[key] = False


def initialise():
    remote.bind_all(register_input)
    remote.listen()


def cleanup():
    remote.unbind_all(register_input)
