import numpy as np
import pygame
from pygame import gfxdraw
from constants import colors
from constants import PERSON_RADIUS

class Person:
    def __init__(self, win):
        self.x_pos = np.random.random_sample()*(win.get_width() - PERSON_RADIUS) + PERSON_RADIUS/2
        self.y_pos = np.random.random_sample()*(win.get_height() - PERSON_RADIUS) + PERSON_RADIUS/2

        self.x_vel = np.random.random_sample()*5
        self.y_vel = np.random.random_sample()*5

        self.x_accel = 0
        self.y_accel = 0

        self.state = 0

    def update(self, win):
        self.edges(win)
        self.movement()
        pygame.draw.circle(win, colors['b'], (int(self.x_pos), int(self.y_pos)), PERSON_RADIUS)

    # objects will bounce off the edge
    def edges(self, win):
        if self.x_pos - PERSON_RADIUS <= 0:
            self.x_vel = (-1) * self.x_vel
        if self.y_pos - PERSON_RADIUS <= 0:
            self.y_vel = (-1) * self.y_vel
        if self.x_pos + PERSON_RADIUS >= win.get_width():
            self.x_vel = (-1) * self.x_vel
        if self.y_pos + PERSON_RADIUS >= win.get_height():
            self.y_vel = (-1) * self.y_vel

    def movement(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel