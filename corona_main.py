import pygame
from pygame import gfxdraw
from person import Person
from constants import colors

pygame.init()

display_width = 1600
display_height = 900

window = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption("Corona")
clock = pygame.time.Clock()

run = True
while run:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        # print(event)

    # green middle vertical line
    pygame.gfxdraw.line(window, int(window.get_width()/2), 0, int(window.get_width()/2), int(window.get_height()), colors['g'])
    pygame.display.update()

    clock.tick(60)

pygame.quit()
