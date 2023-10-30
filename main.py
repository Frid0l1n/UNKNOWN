import pygame
from pygame.locals import *
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

player_rect = pygame.Rect(640, 360, 20, 20)  # Create a player rectangle

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill("black")

    pygame.draw.circle(screen, "red", player_rect.center, 10)

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Calculate the direction vector
    direction = [mouse_x - player_rect.centerx, mouse_y - player_rect.centery]

    length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
    if length != 0:
        direction = [direction[0] / length, direction[1] / length]

    pygame.draw.line(screen, (255, 255, 0), player_rect.center,
                     (player_rect.centerx + direction[0] * 100, player_rect.centery + direction[1] * 100), 5)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= 3
    if keys[pygame.K_s]:
        player_rect.y += 3
    if keys[pygame.K_a]:
        player_rect.x -= 3
    if keys[pygame.K_d]:
        player_rect.x += 3

    pygame.display.flip()
    clock.tick(60)

pygame.quit()