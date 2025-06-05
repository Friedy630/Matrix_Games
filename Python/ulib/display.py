from ulib import pygame_emulator


def set_xy(pixel: tuple, color: tuple):
    pygame_emulator.set_xy(*pixel, color)


def fill(color: tuple):
    pygame_emulator.fill(color)


def show():
    pygame_emulator.show()
