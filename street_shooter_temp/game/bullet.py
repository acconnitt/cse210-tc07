# Imports arcade library
import arcade
# From contastants import all
from game.constants import *
# Import flying_object imports Flying_Object
from game.flying_object import Flying_Object


class Bullet(Flying_Object):
    """Standard Bullet that fires from the shooter, and can only collide 
    with target. It will be removed after a set distance. """

    def __init__(self):
        super().__init__()
        self.speed = BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.velocity.dy = BULLET_SPEED
        self.velocity.dx = 0

    def draw(self, shooter):
        """draws the bullet sprite. """
        # Bullet image
        img = "assets/laserBlue01.png"
        texture = arcade.load_texture(img)

        width = texture.width
        height = texture.height
        alpha = 255

        # Bullet Angles
        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_texture_rectangle(
            x, y, width, height, texture, angle, alpha)
