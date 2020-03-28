import numpy as np
import pygame
from constants import colors
from constants import RADIUS
from constants import MAX_VEL
from constants import MAX_ACCEL

# TODO: they go towards bottom

class Person:
    def __init__(self, win):
        self.x_pos = np.random.random_sample()*(win.get_width() - RADIUS) + RADIUS/2
        self.y_pos = np.random.random_sample()*(win.get_height() - RADIUS) + RADIUS/2

        self.x_vel = np.random.random_sample()*MAX_VEL
        self.y_vel = np.random.random_sample()*MAX_VEL

        self.x_accel = 0
        self.y_accel = 0

        self.state = 0

        self.perception = 50
        self.steering_speed = 1

    def draw(self, win):
        pygame.draw.circle(win, colors['b'], (int(self.x_pos), int(self.y_pos)), RADIUS)


    def update(self, win, people):
        self.distancing(people, self.perception, self.steering_speed)
        # self.collision_detection(people)
        self.edges(win)
        self.limit_accel()
        self.accelerate()
        self.limit_speed()
        self.movement()
        # print(self.x_vel, self.y_vel)
        self.draw(win)


# TODO: steer speed
    def distancing(self, people, perc, steer):
        steering = np.zeros((2))
        count = 0
        for other in people:
            if self is other:
                continue
            d = np.sqrt((self.x_pos - other.x_pos) ** 2 + (self.y_pos - other.y_pos) ** 2)
            if d < perc:
                diff = np.array([self.x_pos - other.x_pos, self.y_pos - other.y_pos])
                diff = diff / (d**2)
                steering += diff
                count += 1
        if count != 0:
            steering /= count
            mag = np.linalg.norm(steering)
            steering = steering * MAX_VEL / mag
            steering -= np.array([self.x_vel, self.y_vel])
        self.x_accel += steering[0]
        self.y_accel += steering[1]

    # objects will bounce off the edge, and given opposite velocity and acceleration etc
    def edges(self, win):
        if self.x_pos - RADIUS <= 0:
            self.x_vel = -self.x_vel
            self.x_accel = -self.x_accel
            self.x_pos = RADIUS
        if self.y_pos - RADIUS <= 0:
            self.y_vel = -self.y_vel
            self.y_accel = -self.y_accel
            self.y_pos = RADIUS
        if self.x_pos + RADIUS >= win.get_width():
            self.x_vel = -self.x_vel
            self.x_accel = -self.x_accel
            self.x_pos = win.get_width() - RADIUS
        if self.y_pos + RADIUS >= win.get_height():
            self.y_vel = -self.y_vel
            self.y_accel = -self.y_accel
            self.y_pos = win.get_height() - RADIUS

    def accelerate(self):
        self.x_vel += self.x_accel
        self.y_vel += self.y_accel

    def movement(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        if np.absolute(self.x_vel) > MAX_VEL or np.absolute(self.y_vel) > MAX_VEL:
            print("SIR YOU'RE OVER THE SPEED LIMIT")

    def collision_detection(self, people):
        for other in people:
            if self is other:
                continue
            d = np.sqrt((self.x_pos - other.x_pos)**2 + (self.y_pos - other.y_pos)**2)
            if d/2 < RADIUS:
                self.collide(other)

    def collide(self, other):
        self_speed = np.sqrt(self.x_vel**2 + self.y_vel**2)
        other_speed = np.sqrt(other.x_vel**2 + other.y_vel**2)
        x_diff = -(self.x_pos - other.x_pos)
        y_diff = -(self.y_pos - other.y_pos)

        if x_diff > 0:
            if y_diff > 0:
                angle = np.degrees(np.arctan(y_diff / x_diff))
                x_new = -self_speed * np.cos(np.radians(angle))
                y_new = -self_speed * np.sin(np.radians(angle))
            elif y_diff < 0:
                angle = np.degrees(np.arctan(y_diff / x_diff))
                x_new = -self_speed * np.cos(np.radians(angle))
                y_new = -self_speed * np.sin(np.radians(angle))
        elif x_diff < 0:
            if y_diff > 0:
                angle = 180 + np.degrees(np.arctan(y_diff / x_diff))
                x_new = -self_speed * np.cos(np.radians(angle))
                y_new = -self_speed * np.sin(np.radians(angle))
            elif y_diff < 0:
                angle = -180 + np.degrees(np.arctan(y_diff / x_diff))
                x_new = -self_speed * np.cos(np.radians(angle))
                y_new = -self_speed * np.sin(np.radians(angle))
        elif x_diff == 0:
            if y_diff > 0:
                angle = -90
            else:
                angle = 90
            x_new = self_speed * np.cos(np.radians(angle))
            y_new = self_speed * np.sin(np.radians(angle))
        elif y_diff == 0:
            if x_diff < 0:
                angle = 0
            else:
                angle = 180
            x_new = self_speed * np.cos(np.radians(angle))
            y_new = self_speed * np.sin(np.radians(angle))
        self.x_vel = x_new
        self.y_vel = y_new

    def limit_accel(self):
        if self.x_accel > MAX_ACCEL:
            self.x_accel = MAX_ACCEL
        elif self.x_accel < -MAX_ACCEL:
            self.x_accel = -MAX_ACCEL
        if self.y_accel > MAX_ACCEL:
            self.y_accel = MAX_ACCEL
        elif self.y_accel < -MAX_ACCEL:
            self.y_accel = -MAX_ACCEL

    def limit_speed(self):
        if self.x_vel > MAX_VEL:
            self.x_vel = MAX_VEL
        elif self.x_vel < -MAX_VEL:
            self.x_vel = -MAX_VEL
        if self.y_vel > MAX_VEL:
            self.y_vel = MAX_VEL
        elif self.y_vel < -MAX_VEL:
            self.y_vel = -MAX_VEL