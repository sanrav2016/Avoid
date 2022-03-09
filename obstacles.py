# Obstacles.py
# Manages the dots, or "obstacles"
# Note: the dots were initially supposed to be obstacles that decreased the player's health

import pygame, random, mechanics, screen, levels

class Obstacle():
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.motion = mechanics.Linear_Motion()
        self.color = screen.colors["white"]

    def draw(self, time):
        coord = self.motion.coordinate(time)
        self.rect.left, self.rect.top = coord
        pygame.draw.circle(screen.surface, self.color, coord, 3, 3)

obstacles_list = []
# Function to generate obstacles for each new level
# Based on randomness and ensures no playthrough of a level will be the exact same
# The same principle is used for the void
def generate_obstacles():
    global obstacles_list
    obstacles_list = []
    for i in range(50):
        obstacle = Obstacle(image="", rect=pygame.Rect(0, 0, 5, 5))
        origin = random.randrange(0, screen.width), random.randrange(0, screen.height)
        v = [random.randrange(-50, 50), random.randrange(-50, 50)]
        obstacle.motion.change_motion(time=0,
                                      origin=origin,
                                      init_velocity_x=v[0],
                                      init_velocity_y=v[1],
                                      acceleration_x=0,
                                      acceleration_y=0)
        obstacles_list.append(obstacle)

def draw_obstacles(time):
    for obstacle in obstacles_list:
        obstacle.draw(time)
        x, y = obstacle.motion.coordinate(time)
        if x < 0 or x > screen.width:
            obstacle.motion.change_motion(time, init_velocity_x=-obstacle.motion.init_velocity_x)
        if y < 0 or y > screen.height:
            obstacle.motion.change_motion(time, init_velocity_y=-obstacle.motion.init_velocity_y)

# Checks if the player collides with the dot to give the player health
# The function for collision is in Mechanics.py
def check_collide(player):
    level = levels.levels[levels.level]
    for obstacle in obstacles_list:
        if mechanics.rect_collide(player.rect, obstacle.rect):
            player.health += level.gain
            if player.health > 100: player.health = 100
            origin = random.randrange(0, screen.width), random.randrange(0, screen.height)
            v = [random.randrange(-50, 50), random.randrange(-50, 50)]
            obstacle.motion.change_motion(time=0,
                                          origin=origin,
                                          init_velocity_x=v[0],
                                          init_velocity_y=v[1],
                                          acceleration_x=0,
                                          acceleration_y=0)