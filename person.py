import numpy as np
import pygame
from scipy.spatial.distance import pdist
from settings import *

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

        self.distances = {}

    def draw(self, win):
        # Draw person as circle
        pygame.draw.circle(win, COLORS[self.state], (int(self.x_pos), int(self.y_pos)), RADIUS)
        # SHOWS INFECTION RADIUS
        # pygame.draw.circle(win, COLORS[5], (int(self.x_pos), int(self.y_pos)), self.rad_i, 1)

        # Draw velocity vector
        if SHOW_VELOCITY:
            pygame.draw.aaline(win, COLORS[3], (int(self.x_pos), int(self.y_pos)),
                               (int(self.x_pos + 5 * self.x_vel), int(self.y_pos + 5 * self.y_vel)))


    def update(self, win, people, distances):
        self.distancing(people, distances, self.perception, self.steering_speed)
        self.infection(people, distances)
        # self.collision_detection(people)

        # applying speeds and cleaning up
        self.accel_polish()
        self.edges(win)
        self.limit_accel()
        self.accelerate()
        self.limit_speed()
        self.movement()

        self.draw(win)

    def infection(self, people, distances):
        # able to infect others
        if self.state == 1 or self.state == 2:
            for other in people:
                if self is other:
                    continue
                d = distances[min(people.index(self), people.index(other)),
                              max(people.index(self), people.index(other))]
                if d < self.rad_i:
                    # exponential distribution
                    if np.random.random_sample() < (1-np.exp(-self.rate_i/FRAME))\
                            and other.state == 0:
                        other.state = 1



    def distancing(self, people, distances, perc, steer):
        steering = np.zeros((2))
        count = 0
        for other in people:
            if self is other:
                continue
            # d = np.sqrt((self.x_pos - other.x_pos) ** 2 + (self.y_pos - other.y_pos) ** 2)
            d = distances[min(people.index(self), people.index(other)),
                          max(people.index(self), people.index(other))]
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
        self.x_accel, self.y_accel = self.x_accel + steer * steering[0], self.y_accel + steer * steering[1]


    # NOW IMPLEMENTED IN helper_funcs.py SO IT'S CALLED EVERY FRAME RATHER THAN EVERY OBJECTS
    """    def get_distance(self, people):
        locs = []
        for other in people:
            locs.append([other.x_pos, other.y_pos])
        d = np.array(pdist(locs))
        index = 0
        for i in range(len(people)):
            for j in range(i+1, len(people)):
                self.distances[i, j] = d[index]
    index += 1
    """


    # polishes acceleration by introducing random acc, and decreases accel over time
    def accel_polish(self):
        self.x_accel += (np.random.random_sample()*2 - 1)*MAX_ACCEL*RANDOM_ACCEL_COE
        self.y_accel += (np.random.random_sample()*2 - 1)*MAX_ACCEL*RANDOM_ACCEL_COE

        self.x_accel, self.y_accel = self.x_accel * ACCEL_DECAY, self.y_accel * ACCEL_DECAY

    # ------------------------ SHOULD BE DONE AND DO NOT REQUIRE CHANGES ----------
    # objects will bounce off the edge, and given opposite velocity and acceleration etc
    def edges(self, win):
        if self.x_pos - 0 <= 0:
            self.x_vel *= -1
            self.x_accel *= -1
            self.x_pos = 0
        if self.y_pos - 0 <= 0:
            self.y_vel *= -1
            self.y_accel *= -1
            self.y_pos = 0
        if self.x_pos + 0 >= win.get_width():
            self.x_vel *= -1
            self.x_accel *= -1
            self.x_pos = win.get_width() - 0
        if self.y_pos + 0 >= win.get_height():
            self.y_vel *= -1
            self.y_accel *= -1
            self.y_pos = win.get_height() - 0

    def accelerate(self):
        self.x_vel, self.y_vel = self.x_vel + self.x_accel, self.y_vel + self.y_accel

    def movement(self):
        self.x_pos, self.y_pos = self.x_pos + self.x_vel, self.y_pos + self.y_vel
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
        self.x_vel, self.y_vel = x_new, y_new
