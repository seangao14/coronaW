import pygame
from pygame import gfxdraw
from individual import Person

pygame.init()

display_width = 1600
display_height = 900
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

window = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption("Corona")
clock = pygame.time.Clock()

one_person = Person()

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            widnow = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        # print(event)

    one_person.update(window)

    # green middle vertical line
    pygame.gfxdraw.line(window, int(window.get_width()/2), 0, int(window.get_width()/2), int(window.get_height()), colors['g'])
    pygame.display.update()

    clock.tick(60)

pygame.quit()
