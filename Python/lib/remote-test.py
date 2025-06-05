from ulib import remote, display
import time

x = 0
y = 0


def left(c):
    global x
    x -= 1
    if x < 0:
        x = 15


def right(c):
    global x
    x += 1
    if x > 15:
        x = 0


def up(c):
    global y
    y -= 1
    if y < 0:
        y = 15


def down(c):
    global y
    y += 1
    if y > 15:
        y = 0


remote.bind_all(print)
remote.bind_key("A", left)
remote.bind_key("D", right)
remote.bind_key("W", up)
remote.bind_key("S", down)
remote.listen()

while True:
    display.fade((0, 0.99, 0.99999))
    display.set_xy((x, y), (50, 50, 50))
    display.show()
    time.sleep(0.1)
