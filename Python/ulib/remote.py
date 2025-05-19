from ulib import pygame_emulator
import time

def listen():
    pygame_emulator.listen()

def bind_key(key, action):
    pygame_emulator.bind_key(key, action)

def unbind_key(key, action):
    pygame_emulator.unbind_key(key, action)

def bind_all(action):
    pygame_emulator.bind_all(action)

def unbind_all(action):
    pygame_emulator.unbind_all(action)

def start_pygame_thread():
    pygame_emulator.start_pygame_thread()
    time.sleep(0.1) #warten bis der thread da ist

def close_pygame_thread():
    pygame_emulator.close()