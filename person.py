import numpy as np
import pygame
from constants import colors
from constants import PERSON_RADIUS
import math

class Person:
    def __init__(self, win):
        self.x_pos = np.random.random_sample()*(win.get_width() - PERSON_RADIUS) + PERSON_RADIUS/2
        self.y_pos = np.random.random_sample()*(win.get_height() - PERSON_RADIUS) + PERSON_RADIUS/2

        self.x_vel = np.random.random_sample()*5
        self.y_vel = np.random.random_sample()*5

        self.x_accel = 0
        self.y_accel = 0

        self.state = 0

    def update(self, win, people):

        self.collision_detection(people)
        self.edges(win)
        self.movement()
        pygame.draw.circle(win, colors['b'], (int(self.x_pos), int(self.y_pos)), PERSON_RADIUS)

    # objects will bounce off the edge
    def edges(self, win):
        if self.x_pos - PERSON_RADIUS <= 0:
            self.x_vel = -self.x_vel
        if self.y_pos - PERSON_RADIUS <= 0:
            self.y_vel = -self.y_vel
        if self.x_pos + PERSON_RADIUS >= win.get_width():
            self.x_vel = -self.x_vel
        if self.y_pos + PERSON_RADIUS >= win.get_height():
            self.y_vel = -self.y_vel

    def movement(self):
        self.x_vel += self.x_accel
        self.y_vel += self.y_accel
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def collision_detection(self, people):
        for other in people:
            if self is other:
                continue
            d = np.sqrt((self.x_pos - other.x_pos)**2 + (self.y_pos - other.y_pos)**2)
            if d/2 < PERSON_RADIUS:
                self.collide(other)

    def collide(self, other):
        self_speed = np.sqrt(self.x_vel**2 + self.y_vel**2)
        other_speed = np.sqrt(other.x_vel**2 + other.y_vel**2)
        x_diff = -(self.x_pos - other.x_pos)
        y_diff = -(self.y_pos - other.y_pos)

        if x_diff > 0:
            if y_diff > 0:
                angle = math.degrees(math.atan(y_diff / x_diff))
                x_new = -self_speed * math.cos(math.radians(angle))
                y_new = -self_speed * math.sin(math.radians(angle))
            elif y_diff < 0:
                angle = math.degrees(math.atan(y_diff / x_diff))
                x_new = -self_speed * math.cos(math.radians(angle))
                y_new = -self_speed * math.sin(math.radians(angle))
        elif x_diff < 0:
            if y_diff > 0:
                angle = 180 + math.degrees(math.atan(y_diff / x_diff))
                x_new = -self_speed * math.cos(math.radians(angle))
                y_new = -self_speed * math.sin(math.radians(angle))
            elif y_diff < 0:
                angle = -180 + math.degrees(math.atan(y_diff / x_diff))
                x_new = -self_speed * math.cos(math.radians(angle))
                y_new = -self_speed * math.sin(math.radians(angle))
        elif x_diff == 0:
            if y_diff > 0:
                angle = -90
            else:
                angle = 90
            x_new = self_speed * math.cos(math.radians(angle))
            y_new = self_speed * math.sin(math.radians(angle))
        elif y_diff == 0:
            if x_diff < 0:
                angle = 0
            else:
                angle = 180
            x_new = self_speed * math.cos(math.radians(angle))
            y_new = self_speed * math.sin(math.radians(angle))
        self.x_vel = x_new
        self.y_vel = y_new

        
        