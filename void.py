# Void.py
# Code for the void behavior

import pygame, random, math, mechanics, screen, levels

# Void class
class Void():
    def __init__(self, rect):
        self.rect = rect
        self.motion = mechanics.Circular_Motion(origin=screen.center)
        self.color = screen.colors["black"]
        self.hover_color = screen.colors["black"]
        self.angle_offset = math.pi / 20
        self.collide = False
        self.reflect = []
        self.curve_offset = 100000

    # The void is just a point which follows circular motion
    # It is drawn using several arcs which are bunched closely together and move as one
    # Note: we initially tried to use adjacent lines but it did not look that good
    # It forms a sector shape
    def draw(self, time):
        self.rect.left, self.rect.top = self.motion.coordinate(time)
        angle = self.motion.angle(time)
        diagonal = math.sqrt(screen.width ** 2 + screen.height ** 2)
        draw_range = diagonal / 2
        time_range = 3
        if time < time_range and levels.level != 6:
            draw_range *= (time / time_range)
        curve_offset = self.curve_offset if self.curve_offset != 0 else 100000
        origin = list(self.motion.origin)
        for i in range(0, round(draw_range)):
            rect = pygame.Rect(origin[0] - i, origin[1] - i, i * 2, i * 2)
            angle1 = -(angle + self.angle_offset + i / curve_offset)
            angle2 = -(angle - self.angle_offset + i / curve_offset)
            color = self.color
            if self.collide: color = self.hover_color
            pygame.draw.arc(screen.surface, color, rect, angle1, angle2)
            # Handling reflections of the void
            # Reflections are present in Levels.py
            for r in self.reflect:
                new_angle1 = angle1 + r
                new_angle2 = angle2 + r
                pygame.draw.arc(screen.surface, color, rect, new_angle1, new_angle2)

    # Custom change motion function which connects to the original change motion function in Mechanics.py
    # This is a custom made function to simplify void behavior at the start of each level
    # It can also be made to manipulate the data set by the original function
    def change_motion(self, time, origin=None, angle=None, v=None, a=None):
        if origin == None and angle == None and v == None and a == None:
            level = levels.levels[levels.level]
            if abs(round(self.motion.current_velocity(time), 4)) <= 1:
                v = random.randrange(level.v[0], level.v[1])
                i = 1
                if v < 0: i = -1
                a = -i * random.randrange(level.a[0], level.a[1])
                if v == 0: a = 0
                self.motion.change_motion(time=time, init_velocity=v, acceleration=a)
        else:
            if origin == None: origin = self.motion.origin
            if angle == None: angle = self.motion.angle(time)
            if v == None: v = self.motion.current_velocity(time)
            if a == None: a = self.motion.acceleration
            self.motion.change_motion(time=time, origin=origin, init_velocity=v, acceleration=a, start_angle=angle)

    # Functions used in different levels

    def change_size(self, change):
        self.angle_offset += change

    def change_curve_offset(self, change, goal=None):
        if goal:
            if self.curve_offset != goal: self.curve_offset += change
        else:
            self.curve_offset += change

    def change_color(self, goal, change=None):
        if self.color != goal:
            l = list(self.color)
            q = []
            for i, x in enumerate(l):
                if change != None: q.append(x + change)
                else: q.append(goal[i])
            self.color = tuple(q)

    def set_reflect(self, arr):
        self.reflect = arr

    # Important!
    # Checks to see if the player collides with the void
    # This is done simply by seeing if the angle of the player is between the two angles of the void
    def check_collide(self, time, player):
        void_angle = self.motion.angle(time) % (2 * math.pi)
        player_angle = player.motion.angle(time) % (2 * math.pi)
        crash = abs(void_angle - player_angle) < self.angle_offset
        if not crash and len(self.reflect) > 0:
            for r in self.reflect:
                new_void_angle = void_angle + r
                crash = abs(new_void_angle - player_angle) < self.angle_offset
                if crash: break
        if crash:
            self.collide = True
        else: self.collide = False