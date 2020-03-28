import pygame
from person import Person
from constants import colors

pygame.init()

display_width = 1600
display_height = 900

window = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption("Corona")
clock = pygame.time.Clock()

community = pygame.Surface((int(window.get_width()/2-1), int(window.get_height())))

test_people = []

for i in range(20):
    test_people.append(Person(community))


run = True
while run:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        # print(event)

    # draw
    community = pygame.Surface((int(window.get_width() / 2 - 1), int(window.get_height())))

    for i in test_people:
        i.update(community, test_people)

    window.blit(community, (int(window.get_width() / 2 + 1), 0))
    # green middle vertical line
    pygame.draw.line(window, colors['g'], (window.get_width()/2, 0), (window.get_width()/2, window.get_height()), 2)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
