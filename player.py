# Player.py
# Code for the player behavior

import pygame, mechanics, math, screen

# Player class
class Player():
    def __init__(self, rect):
        self.rect = rect
        self.motion = mechanics.Circular_Motion(origin=screen.center)
        self.control_key_press = False
        self.frame = 0
        self.health = 100

    # There is a set of 59 images of a rocket's engine blowing smoke out
    # The program loops through these images continuously to provide the animation
    # This is only run when the "space" key is pressed;
    # otherwise the image reverts to the first one where there is no smoke
    def draw(self, time):
        coord = self.motion.coordinate(time)
        self.rect.left, self.rect.top = coord
        screen.image("images/player/" + str(self.frame) + ".png", coord, scale=0.2, rotate=math.pi - (self.motion.angle(time) % (2 * math.pi)))
        if self.control_key_press:
            self.frame += 1
        else:
            self.frame = 0
        if self.frame == 60: self.frame = 1

    # Binding space to player motion - the below two functions

    def control(self, time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.control_key_press = True
            self.motion.change_motion(time, acceleration=1)
        else:
            self.control_key_press = False

    def change_motion(self, time):
        if self.control_key_press == True:
            if abs(round(self.motion.current_velocity(time), 4) - 6) <= 0.01:
                self.motion.change_motion(time, acceleration=0)
        elif self.control_key_press == False:
            self.motion.change_motion(time, acceleration=-1)
            if round(self.motion.current_velocity(time), 4) == 0:
                self.motion.change_motion(time, acceleration=0)