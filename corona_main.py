import pygame
from pygame import gfxdraw
from individual import Person
from constants import colors

pygame.init()

display_width = 1600
display_height = 900

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
