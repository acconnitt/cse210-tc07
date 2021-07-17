# Imports arcade library
import arcade
# From constants import all
from game.constants import *
# Import flying_object imports Flying_Object
from game.flying_object import Flying_Object


class Shooter(Flying_Object):
    """Creates and control the shooter"""

    def __init__(self):
        super().__init__()

        self.radius = SHOOTER_RADIUS
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = 0 + SHOOTER_SIZE
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.fire_rate = BULLET_FIRE_RATE
        self.lives = START_LIVES
        self.damage = 1

    def move_right(self):
        """Move to the right"""
        if self.center.x < SCREEN_WIDTH - SHOOTER_SIZE / 2:
            self.velocity.dx = 1 * SHOOTER_SPEED
        else:
            self.center.x = SCREEN_WIDTH - SHOOTER_SIZE / 2

    def move_left(self):
        """Move to the left"""
        if self.center.x > 0 + SHOOTER_SIZE / 2:
            self.velocity.dx = -1 * SHOOTER_SPEED
        else:
            self.center.x = 0 + SHOOTER_SIZE / 2

    def collide(self):
        """Handle collisions"""
        self.lives -= 1
        if self.lives <= 0:
            """Determine if shooter is alive"""
            self.alive = False

    def draw(self):
        """Display the alive and dead shooter"""

        img = "assets/alive_shooter.png"
        texture = arcade.load_texture(img)
        img_hit = "assets/dead_shooter.png"
        texture2 = arcade.load_texture(img_hit)

        width = texture.width / 8
        height = texture.height / 8
        alpha = 255
        x = self.center.x
        y = self.center.y
        angle = self.angle + 90

        arcade.draw_text(f"Power: {self.damage}", SCREEN_WIDTH*.8,
                         SCREEN_HEIGHT*.95, arcade.color.PURPLE_HEART, 20)

        arcade.draw_text(f"Lives: {self.lives}", 15,
                         SCREEN_HEIGHT*.9, arcade.color.RED, 20)
        if self.alive:
            arcade.draw_texture_rectangle(
                x, y, width, height, texture, angle, alpha)

        else:
            arcade.draw_texture_rectangle(
                x + 10, y+5, 50, 50, texture2, angle, alpha)
