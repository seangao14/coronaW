import numpy as np
import pygame
from pygame import gfxdraw

colors = {
    'r': (255, 0, 0), # red
    'g': (0, 255, 0), # green
    'b': (0, 0, 255), # blue
    'y': (255, 255, 0), # yellow
    'c': (0, 255, 255), # cyan
    'm': (255, 0, 255), # magenta
    'w': (255, 255, 255), # white
    'k': (0, 0, 0) # black
}

class Person:
    def __init__(self):
        self.x_pos = 100
        self.y_pos = 100

    def update(self, window_):
        pass
