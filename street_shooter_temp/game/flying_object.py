# From point import Point
from game.point import Point
#from velocity import Velocity
from game.velocity import Velocity
# From abc library import ABCMeta and abstractmethod
from abc import ABCMeta, abstractmethod


class Flying_Object():
    """Creates an object with a center point, velocity, and radius. Also stores a 
    variable that tells if it should remain on the board after being hit, or when 
    to remove an object when it is offscreen."""

    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 1.0
        self.alive = True
        self.angle = 0
        self.speed = 0

    def advance(self):
        """Changes object location by adding velocity to the Point Coordinates"""
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_off_screen(self, screen_width, screen_height, radius):
        """Determines if object off screen"""
        if (self.center.x > screen_width + radius):
            self.center.x = 0 - radius

        if (self.center.x < 0 - radius):
            self.center.x = screen_width + radius

        if (self.center.y > screen_height + radius):
            self.center.y = 0 - radius

        if (self.center.y < 0 - radius):
            self.center.y = screen_height + radius

    def collide(self):
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def collide(self):
        pass
