# Mechanics.py
# Defines linear and circular motion mechanics

import math

# Simple collision function used for the dots
def rect_collide(rect1, rect2):
    crash = True
    if rect1.top + rect1.height < rect2.top or rect1.top > rect2.top + rect2.height or rect1.left + rect1.width < rect2.left or rect1.left > rect2.left + rect2.width:
        crash = False
    return crash

# Linear motion, used for the dots
class Linear_Motion():
    def __init(self, origin=(0, 0), init_velocity_x=0, init_velocity_y=0, acceleration_x=0, acceleration_y=0):
        self.origin = origin
        self.init_velocity_x = init_velocity_x
        self.init_velocity_y = init_velocity_y
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.reset = 0

    def current_velocity_vector(self, time):
        time -= self.reset
        return [self.init_velocity_x + self.acceleration_x * time,
                self.init_velocity_y + self.acceleration_y * time]

    # Coordinate changes with time, which is used to draw the dots
    # Takes into account acceleration, although the dots do not accelerate.
    # This is for the purpose of scalability and uniformity
    def coordinate(self, time):
        time -= self.reset
        x = list(self.origin)[0] + self.init_velocity_x * time + 0.5 * self.acceleration_x * time ** 2
        y = list(self.origin)[1] + self.init_velocity_y * time + 0.5 * self.acceleration_y * time ** 2
        return x, y

    def change_motion(self, time, origin=None, init_velocity_x=None, init_velocity_y=None, acceleration_x=None, acceleration_y=None):
        if origin != None: self.origin = origin
        else: self.origin = self.coordinate(time)
        if init_velocity_x != None: self.init_velocity_x = init_velocity_x
        if init_velocity_y != None: self.init_velocity_y = init_velocity_y
        if acceleration_x != None: self.acceleration_x = acceleration_x
        if acceleration_y != None: self.acceleration_y = acceleration_y
        self.reset = time

# Circular motion, used for player and void
class Circular_Motion():
    def __init__(self, origin=(0, 0), radius=0, init_velocity=0, acceleration=0, start_angle=0):
        self.origin = origin
        self.radius = radius
        self.init_velocity = init_velocity
        self.acceleration = acceleration
        self.start_angle = start_angle
        self.reset = 0

    def current_velocity(self, time):
        time -= self.reset
        return self.init_velocity + self.acceleration * time

    # Separate coordinate into polar coordinate (angle) and Cartesian coordinate (coordinate)
    def angle(self, time):
        time -= self.reset
        return self.start_angle + self.init_velocity * time + 0.5 * self.acceleration * time ** 2

    def coordinate(self, time):
        angle = self.angle(time)
        x = self.radius * math.cos(angle) + list(self.origin)[0]
        y = self.radius * math.sin(angle) + list(self.origin)[1]
        return x, y

    def change_motion(self, time, origin=None, radius=None, init_velocity=None, acceleration=None, start_angle=None):
        if start_angle != None: self.start_angle = start_angle
        else: self.start_angle = self.angle(time)
        if origin != None: self.origin = origin
        if radius != None: self.radius = radius
        if init_velocity != None: self.init_velocity = init_velocity
        else: self.init_velocity = self.current_velocity(time)
        if acceleration != None: self.acceleration = acceleration
        self.reset = time
