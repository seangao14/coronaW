import pygame
from collections import defaultdict
from settings import *

def grapher(win, people, frame, heights):
    win.fill((0,0,0))

    counter = defaultdict(int)
    for i in people:
        counter[i.state] += 1
    # print(counter)

    heights.append(counter)
    for i in range(frame):
        # issues so far:
        #   not saving old data
        #   shows that 100% of pop is red before it actually is (maybe because of int typecast truncation)

        pygame.draw.rect(win, COLORS[0], (int(win.get_width()/frame*i), # x
                                          0,                            # y
                                          win.get_width()/frame,        # width
                                          int(win.get_height()/len(people)*heights[i][0])))      # height

        pygame.draw.rect(win, COLORS[1], (int(win.get_width() / frame * i),  # x
                                          int(win.get_height() / len(people) * heights[i][0]),  # y
                                          win.get_width() / frame,  # width
                                          int(win.get_height() - win.get_height() / len(people) * heights[i][0])))  # height
