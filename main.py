import pygame
from pygame.locals import *
import math
import random
from collections import deque
from math import sin, cos, radians

# Maze setup
maze_width, maze_height = 40, 20
cell_size = 40
maze = [[1 for _ in range(maze_width)] for _ in range(maze_height)]

# Stack for iterative maze generation
stack = deque()

# Maze generator function (Iterative Backtracking)
def generate_maze():
    start_x, start_y = random.randint(0, maze_width - 1), random.randint(0, maze_height - 1)
    stack.append((start_x, start_y))

    while stack:
        x, y = stack.pop()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze[ny][nx] == 1:
                maze[y][x] |= (1 << directions.index((dx, dy)))
                maze[ny][nx] |= (1 << directions.index((-dx, -dy)))
                stack.append((nx, ny))

generate_maze()

def rotate_vector(vector, angle):
        x = vector[0]*math.cos(angle)-vector[1]*math.sin(angle)
        y = vector[0]*math.sin(angle)+vector[1]*math.cos(angle)
        return [x, y]

def pie(scr, color, center, radius, start_angle, stop_angle):
    theta = start_angle
    while theta <= stop_angle:
        pygame.draw.line(scr, color, center,
                             (center[0]+radius*cos(radians(theta)), center[1]+radius*sin(radians(theta))), 2)
        theta += 0.01




# Pygame setup
pygame.init()
screen = pygame.display.set_mode((maze_width * cell_size, maze_height * cell_size), RESIZABLE)
clock = pygame.time.Clock()
running = True

# Set the player's starting position inside the maze
player_x, player_y = random.randint(0, maze_width - 1), random.randint(0, maze_height - 1)
player_rect = pygame.Rect(player_x * cell_size, player_y * cell_size, cell_size, cell_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    screen.fill((0, 0, 0))

    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] & 1 == 0:  # Check right wall
                pygame.draw.line(screen, (255, 255, 255), (x * cell_size + cell_size, y * cell_size),
                                 (x * cell_size + cell_size, y * cell_size + cell_size), 5)
            if maze[y][x] & 2 == 0:  # Check left wall
                pygame.draw.line(screen, (255, 255, 255), (x * cell_size, y * cell_size),
                                 (x * cell_size, y * cell_size + cell_size), 5)
            if maze[y][x] & 4 == 0:  # Check bottom wall
                pygame.draw.line(screen, (255, 255, 255), (x * cell_size, y * cell_size + cell_size),
                                 (x * cell_size + cell_size, y * cell_size + cell_size), 5)
            if maze[y][x] & 8 == 0:  # Check top wall
                pygame.draw.line(screen, (255, 255, 255), (x * cell_size, y * cell_size),
                                 (x * cell_size + cell_size, y * cell_size), 5)

    pygame.draw.circle(screen, (255, 0, 0), player_rect.center, 10)

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Calculate the direction vector
    direction = [mouse_x - player_rect.centerx, mouse_y - player_rect.centery]

    length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
    cone_angle = 45
    side_length = length/(math.cos(cone_angle/2))

    
    if length != 0:
        puffer = direction
        direction = [direction[0] / length, direction[1] / length]
        side_direction = [puffer[0] / side_length, puffer[1] / side_length]

    side_vector1 = rotate_vector(side_direction, cone_angle/2)
    side_vector2 = rotate_vector(side_direction, -cone_angle/2)

    pygame.draw.polygon(screen, (255, 255, 0),
                        [
        player_rect.center,
        (player_rect.centerx + side_vector1[0] * 132,
         player_rect.centery + side_vector1[1] * 132),
        (player_rect.centerx + side_vector2[0] * 132,
         player_rect.centery + side_vector2[1] * 132)
    ], 0)

    circle_center = player_rect.centerx + \
        direction[0] * 100, player_rect.centery + direction[1] * 100

    if length != 0:
        direction_angle = math.atan2(direction[0], direction[1])

        half_circle_angle = 180
        start_angle = direction_angle - half_circle_angle/2
        end_angle = direction_angle + half_circle_angle/2
        RADIUS = 100 * math.tan(cone_angle/2)

        if direction[0] == 0:  # still a bug rotating by 90 degrees right
            direction[0] = 0.0001

        else:
            direction_angle = math.degrees(
                math.atan(direction[1]/direction[0]))

        if direction[0] <= 0:
            direction_angle = direction_angle + 180

        pie(screen, (255, 255, 0), (player_rect.centerx + 100 * direction[0], player_rect.centery + 100 * direction[1]),
            RADIUS, direction_angle-90, direction_angle+90)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        new_rect = player_rect.move(0, -cell_size)
        if all(maze[ny][nx] & 8 == 0 for nx in range(new_rect.left // cell_size, new_rect.right // cell_size)
                for ny in range(new_rect.top // cell_size, new_rect.bottom // cell_size)):
            player_rect = new_rect

    if keys[pygame.K_s]:
        new_rect = player_rect.move(0, cell_size)
        if all(maze[ny][nx] & 4 == 0 for nx in range(new_rect.left // cell_size, new_rect.right // cell_size)
                for ny in range(new_rect.top // cell_size, new_rect.bottom // cell_size)):
            player_rect = new_rect

    if keys[pygame.K_a]:
        new_rect = player_rect.move(-cell_size, 0)
        if all(maze[ny][nx] & 1 == 0 for nx in range(new_rect.left // cell_size, new_rect.right // cell_size)
                for ny in range(new_rect.top // cell_size, new_rect.bottom // cell_size)):
            player_rect = new_rect

    if keys[pygame.K_d]:
        new_rect = player_rect.move(cell_size, 0)
        if all(maze[ny][nx] & 2 == 0 for nx in range(new_rect.left // cell_size, new_rect.right // cell_size)
                for ny in range(new_rect.top // cell_size, new_rect.bottom // cell_size)):
            player_rect = new_rect
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
