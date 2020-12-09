import pygame
from person import Person
from helper_funcs import *
from settings import *
from graphing import grapher


def corona_driver():
    pygame.init()

    display_width, display_height = START_WIDTH, START_HEIGHT

    window = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
    pygame.display.set_caption("Corona")
    clock = pygame.time.Clock()

    community = pygame.Surface((int(window.get_width()/2-1), int(window.get_height())))
    graph = pygame.Surface((int(window.get_width()/2-1), int(window.get_height()/2-1)))

    test_people = []
    frames = 1
    heights = []

    for i in range(START_HEALTHY):
        test_people.append(Person(community, 0))
    for i in range(START_INFECTED):
        test_people.append(Person(community, 1))

    run = True
    # ------------------MAIN LOOP-----------------------
    while run:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # print(event)

        # draw surface
        community = pygame.Surface((int(window.get_width() / 2 - 1), int(window.get_height())))
        graph = pygame.Surface((int(window.get_width() / 2 - 1), int(window.get_height() / 2 - 1)))

        distances = get_distance(test_people)
        # update objects
        for i in test_people:
            i.update(community, test_people, distances)

        grapher(window, test_people, frames, heights)

        # add subsurfaces to window
        window.blit(community, (int(window.get_width() / 2 + 1), 0))
        window.blit(graph, (0, 0))
        # green middle vertical line
        pygame.draw.line(window, COLORS[4], (window.get_width() / 2, 0), (window.get_width() / 2, window.get_height()), 2)
        pygame.display.update()

        clock.tick(FRAME)
        print(frames)
        frames += 1

    pygame.quit()



if __name__ == '__main__':
    corona_driver()