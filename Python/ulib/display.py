from ulib import pygame_emulator

def set_xy(x: int, y: int, color: tuple):
    pygame_emulator.set_xy(x, y, color)

def fill(color: tuple):
    pygame_emulator.fill(color)

def show():
    pygame_emulator.show()