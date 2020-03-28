import numpy as np
import pygame
from pygame import gfxdraw
from constants import colors

class Person:
    def __init__(self):
        self.x_pos = 100
        self.y_pos = 100

        self.x_vel = 0
        self.y_vel = 0

        self.x_accel = 0
        self.y_accel = 0

    def update(self, window_):
        pass


