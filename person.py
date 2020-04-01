import numpy as np
import pygame
from scipy.spatial.distance import pdist
from constants import *

class Person:
    def __init__(self, win, s):
        self.x_pos = np.random.random_sample() * (win.get_width() - RADIUS) + RADIUS / 2
        self.y_pos = np.random.random_sample() * (win.get_height() - RADIUS) + RADIUS / 2

        self.x_vel = np.random.random_sample() * MAX_VEL
        self.y_vel = np.random.random_sample() * MAX_VEL

        self.x_accel = 0
        self.y_accel = 0

        self.state = s
        # 0: healthy, 1: infected, 2: asympomatic carrier, 3: immune, 4: dead

        self.perception = START_PERCEPTION
        self.steering_speed = START_STEERING

        self.rad_i = START_RAD_I
        self.rate_i = START_RATE_I

        self.distance_a = np.array([])

    def draw(self, win):
        # Draw person as circle
        pygame.draw.circle(win, COLORS[self.state], (int(self.x_pos), int(self.y_pos)), RADIUS)
        # pygame.draw.circle(win, colors['y'], (int(self.x_pos), int(self.y_pos)), self.perception, 1)

        # Draw velocity vector
        if SHOW_VELOCITY:
            pygame.draw.aaline(win, COLORS[3], (int(self.x_pos), int(self.y_pos)),
                               (int(self.x_pos + 5 * self.x_vel), int(self.y_pos + 5 * self.y_vel)))


    def update(self, win, people):
        self.get_distance(people)

        self.distancing(people, self.perception, self.steering_speed)
        # self.collision_detection(people)
        self.accel_polish()

        self.edges(win)
        self.limit_accel()
        self.accelerate()
        self.limit_speed()
        self.movement()
        # print(self.x_vel, self.y_vel)
        self.draw(win)

    def infection(self, people):
        if self.state == 1 or self.state == 2:
            pass


    # TODO: change indexing such that 1 checks 2, 3...
    #       2 checks 3, 4, etc... so that there are not duplicate calculations
    def distancing(self, people, perc, steer):
        steering = np.zeros((2))
        count = 0
        for other in people:
            if self is other:
                continue
            d = np.sqrt((self.x_pos - other.x_pos) ** 2 + (self.y_pos - other.y_pos) ** 2)
            if d < perc:
                diff = np.array([self.x_pos - other.x_pos, self.y_pos - other.y_pos])
                diff = diff / (d ** 2)
                steering += diff
                count += 1
        if count != 0:
            steering /= count
            mag = np.linalg.norm(steering)
            steering = steering * MAX_VEL / mag
            steering -= np.array([self.x_vel, self.y_vel])
        self.x_accel += steer * steering[0]
        self.y_accel += steer * steering[1]


    # TODO:
    def get_distance(self, people):
        locs = np.array([])
        for other in people:
            locs.append([other.x_pos, other.y_pos])
        return pdist(locs)


    # polishes acceleration by introducing random acc, and decreases accel over time
    def accel_polish(self):
        self.x_accel += (np.random.random_sample()*2 - 1)*MAX_ACCEL/RANDOM_ACCEL_COE
        self.y_accel += (np.random.random_sample()*2 - 1)*MAX_ACCEL/RANDOM_ACCEL_COE
        self.x_accel *= ACCEL_DECAY
        self.y_accel *= ACCEL_DECAY

    # ------------------------ SHOULD BE DONE AND DO NOT REQUIRE CHANGES ----------
    # objects will bounce off the edge, and given opposite velocity and acceleration etc
    def edges(self, win):
        if self.x_pos - 0 <= 0:
            self.x_vel = -self.x_vel
            self.x_accel = -self.x_accel
            self.x_pos = 0
        if self.y_pos - 0 <= 0:
            self.y_vel = -self.y_vel
            self.y_accel = -self.y_accel
            self.y_pos = 0
        if self.x_pos + 0 >= win.get_width():
            self.x_vel = -self.x_vel
            self.x_accel = -self.x_accel
            self.x_pos = win.get_width() - 0
        if self.y_pos + 0 >= win.get_height():
            self.y_vel = -self.y_vel
            self.y_accel = -self.y_accel
            self.y_pos = win.get_height() - 0

    def accelerate(self):
        self.x_vel += self.x_accel
        self.y_vel += self.y_accel

    def movement(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        if abs(self.x_vel) > MAX_VEL or abs(self.y_vel) > MAX_VEL:
            print("SIR YOU'RE OVER THE SPEED LIMIT")

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


    # these methods probably won't be used, just storing them at the bottom
    def collision_detection(self, people):
        for other in people:
            if self is other:
                continue
            d = np.sqrt((self.x_pos - other.x_pos) ** 2 + (self.y_pos - other.y_pos) ** 2)
            if d / 2 < RADIUS:
                self.collide(other)

    def collide(self, other):
        self_speed = np.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        other_speed = np.sqrt(other.x_vel ** 2 + other.y_vel ** 2)
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

