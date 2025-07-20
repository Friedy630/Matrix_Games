# LED Matrix Games

## General

This repository contains an emulator for a 16x16 LED matrix, allowing you to play several classic games such as Tetris, Snake, Pong, Flappy Bird, Dino, and Game of Life.  
The emulator simulates the LED display and supports keyboard input for development and testing.  
On real hardware, input is handled via UDP over local WiFi, and the `remote` and `display` modules must be replaced with their hardware-specific versions.

## Features

-   Modular Python codebase for easy addition of new games
-   Emulator mode for development and testing on any PC
-   Multiple classic games, each implemented as a separate class
-   Simple main menu for game and speed selection
-   Easily extendable for new games or features

# Games

**Tetris:**
Arrange falling blocks to complete rows and score points. The game features multiple difficulty levels and exotic shapes for extra challenge.

**Snake:**
Control a growing snake to collect fruit and avoid collisions with yourself or the walls. The game includes options for wall wrapping and increasing difficulty.

**Pong:**
Classic two-player paddle game where you try to bounce the ball past your opponent. Features smooth paddle movement and animated ball effects.

**Flappy Bird:**
Guide the bird through gaps in moving pipes by flapping at the right moment. The game challenges your timing and reaction skills.

**Dino:**
Jump over obstacles and survive as long as possible in this endless runner inspired by the Chrome offline dinosaur game. The speed increases over time for added difficulty.

**Game of Life:**
A simulation of Conway’s Game of Life, where simple rules create complex patterns. Watch as cells live, die, and evolve on the LED matrix.

## Usage

1. Install Python and the required dependencies (see `requirements.txt` if available).
2. Run `main.py` to start the emulator and select a game.
3. For real hardware, swap out the emulator modules for the hardware-specific `remote` and `display` implementations.

## TODO

For further details and progress, refer to the project view 'Tetris' or the documentation in each game file.
